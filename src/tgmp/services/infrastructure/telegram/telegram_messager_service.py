import asyncio
import threading
from typing import Dict, Any

import config
from api.gemini import upload_file
from telethon import events, TelegramClient

from factories.repository_factory import RepositoryFactory
from factories.service_factory import ServiceFactory
from services.infrastructure.db_service import DbService
from services.infrastructure.telegram.telegram_connect import TelegramConnect
from services.cv_processing_service import CVProcessingService


# TelegramClient Wrapper for project purposes (need to store project's user_id and telegram_client for using inside handlers)
class TeleAnalystTelegramClient:
    def __init__(self, telegram_client: TelegramClient, user_id):
        self.telegram_client = telegram_client
        # save tele_analyst user_id
        self.user_id = user_id



class TelegramMessagerService:
    # set types for fields
    clients: Dict[Any, TeleAnalystTelegramClient]
    repository_factory: RepositoryFactory
    service_factory: ServiceFactory

    def __init__(self):
        self.clients = {}
        self.loop = None
        self.thread = None
        self.is_running = False
        self.db_connection_string = config.DATABASE

    def _start_async_loop(self):
        """Start asyncio loop in new thread"""

        # create factories inside thread (sqlite3 throws errors when trying to use connect from different threads)
        self.repository_factory = RepositoryFactory(self.db_connection_string)
        self.service_factory = ServiceFactory(self.repository_factory)

        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.is_running = True
        self.loop.run_forever()

    def start(self):
        """Start manager in new thread"""
        self.thread = threading.Thread(target=self._start_async_loop, daemon=True)
        self.thread.start()

        while self.loop is None:
            pass

    def stop(self):
        """Stop manager"""
        if self.loop:
            self.loop.call_soon_threadsafe(self.loop.stop)
            self.is_running = False

    async def add_client_async(self, telegram_connect: TelegramConnect, user_id : int):
        """Add client asynchronously"""
        # creating TelegramClient object
        client = await telegram_connect.connect()

        if user_id is None:
            raise ValueError("You must provide user_id to add client")

        tele_analyst_client = TeleAnalystTelegramClient(client, user_id)

        # Register handlers for newly-created client
        self._register_handlers(tele_analyst_client)

        self.clients[user_id] = tele_analyst_client
        print(f"Client for user id \"{user_id}\" was successfully added")

        return tele_analyst_client

    def add_client(self, telegram_connect: TelegramConnect, user_id : int):
        """Add client"""
        future = asyncio.run_coroutine_threadsafe(
            self.add_client_async(telegram_connect, user_id),
            self.loop
        )
        return future.result()

    async def send_message_async(self, client: TelegramClient, recipient, message):
        """Send message through client asynchronously"""
        await client.send_message(recipient, message)

    def send_message(self, client:TelegramClient, recipient, message):
        """Send message through client"""
        future = asyncio.run_coroutine_threadsafe(
            self.send_message_async(client, recipient, message),
            self.loop
        )
        return future.result()

    def get_client_info(self, user_id):
        """Returns client info"""
        if user_id in self.clients:
            client = self.clients[user_id]
            return {
                'client_name': user_id,
                'is_connected': client.telegram_client.is_connected(),
            }
        return None

    def get_telegram_client(self, user_id) -> TelegramClient:
        """Returns client object"""
        if user_id in self.clients:
            return  self.clients[user_id].telegram_client
        return None

    def get_all_clients(self):
        """Returns all client objects"""
        return {name: self.get_client_info(name) for name in self.clients.keys()}


    def _register_handlers(self, client : TeleAnalystTelegramClient):
        """Register handlers for TeleAnalyst client"""

        @client.telegram_client.on(events.NewMessage(incoming=True, from_users='Arkadiy', func=lambda e: e.media is not None))
        async def handle_new_message(event):
            cv = event.message.document
            dosc = await client.download_media(cv, file="../../")
            # file = os.path.basename()
            file_gemini_reference_to_file = upload_file(dosc)
            tags_from_bd = "javascript, react, laravel"
            result = CVProcessingService.get_ai_result(tags_from_bd, file_gemini_reference_to_file)
            print(result)
            # answer = generate_content(event.message.text)
            # if event.is_private and not event.out:
            #     await event.reply(answer)

            print(f"[Client for user_id: {client.user_id}] New message received: {event.message.text}")

        @client.telegram_client.on(events.NewMessage(outgoing=True))
        async def handle_outgoing_message(event):
            if event.is_private:
                await event.reply("Hi! I received your message!")

            self.service_factory.create_user_service().find_user_by_id(client.user_id)

            print(f"[Client for user_id: {client.user_id}] New message received: {event.message.text}")

        # @self.client.on(events.NewMessage(incoming=True, func=lambda e: e.media is not None))
        # async def handle_incoming_message(event):
        #     # answer = generate_content(event.message.text)
        #     # print(f"New message in chat '{chat.title}' from {sender.first_name}: {event.message.text}")
        #     # answer generate_content(event.message.text)
        #     if event.is_private:
        #         await event.reply(answer)
        #
        #     print(f"New message received: {event.message.text}")

        @client.telegram_client.on(events.NewMessage)
        async def new_message_handler(event):
            print(f"[Client for user_id: {client.user_id}] New message received: {event.message.text}")


        @client.telegram_client.on(events.MessageEdited)
        async def edit_message_handler(event):
            print(f"[Client for user_id: {client.user_id}] Message edited: {event.message.text}")

        @client.telegram_client.on(events.ChatAction)
        async def chat_action_handler(event):
            print(f"[Client for user_id: {client.user_id}] Some action happened: {event}")


    async def get_chat_async(self, client: TelegramClient, chat_name: str=None):
        if chat_name is None:
            chat_name = config.CHANNEL_LINK
        chat = await client.get_entity(chat_name)
        return chat

    def get_chat(self, client: TelegramClient, chat_name: str=None):
        future = asyncio.run_coroutine_threadsafe(
            self.get_chat_async(client, chat_name),
            self.loop
        )
        return future.result()

    async def remove_client_async(self, user_id: int):
        """Remove client async"""
        if user_id in self.clients:
            client = self.clients[user_id]

            # Before delete - disconnect client
            await client.telegram_client.disconnect()

            # Remove from client pool
            del self.clients[user_id]
            print(f"[Client for user_id: {client.user_id}] was successfully disconnected and removed")
            return True
        else:
            print(f"Client for user_id: {user_id} was not found")
            return False

    def remove_client(self, user_id: int):
        """Remove client"""
        future = asyncio.run_coroutine_threadsafe(
            self.remove_client_async(user_id),
            self.loop
        )
        return future.result()

#     async def send_video(self):
#         folder = Media("D:\\tv", extensions=[".mp4", ".webm", ".avi"])
#         videos = folder.get_media_files()
#
#         for video in videos:
#             await  self.client.send_file(self.entity, video)
#             print(f"Sent: {video}")
#
#         return {"message": "Video folder retrieved successfully"}
#
#
#     def upload_files(self, files):
#         for file in files:
#             print(f"Uploading {file} to Telegram...")