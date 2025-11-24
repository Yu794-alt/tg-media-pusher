import asyncio
import threading
import uuid
import requests

import config
from api.gemini import generate_content, upload_file
from telethon import events, TelegramClient

from entities.analytic_record_entiry import AnalyticRecord
from entities.candidate_entity import Candidate
# from flask import session, current_app as app

from factories.repository_factory import RepositoryFactory
from factories.service_factory import ServiceFactory
from services.cv_processing_service import CVProcessingService
from services.telegram.telegram_connect import TelegramConnect
from services.user_service import UserService
from utils.helpers.db_connection_helper import DBConnection


class TelegramMessagerService:
    repository_factory: RepositoryFactory
    service_factory: ServiceFactory

    def __init__(self, app):
        self.clients = {}
        self.flask_config = app.config
        self.loop = None
        self.thread = None
        self.is_running = False

    def _start_async_loop(self):
        """Start asyncio loop in new thread"""
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.repository_factory = RepositoryFactory(DBConnection.get_SQL3_connection(config.DATABASE))
        self.service_factory = ServiceFactory(self.repository_factory)
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

    async def add_client_async(self, telegram_connect: TelegramConnect, client_name: str = None):
        """Add client asynchronously"""

        client = await telegram_connect.connect()

        if client_name is None:
            client_name = str(uuid.uuid4())
        # Регистрируем обработчики событий
        self._register_handlers(client, client_name)

        self.clients[client_name] = client
        print(f"Client {client_name} was successfully added")

        return client

    def add_client(self, telegram_connect: TelegramConnect, client_name: str = None):
        """Add client"""
        future = asyncio.run_coroutine_threadsafe(
            self.add_client_async(telegram_connect, client_name),
            self.loop
        )
        return future.result()

    async def send_message_async(self, client, recipient, message):
        """Send message through client asynchronously"""
        await client.send_message(recipient, message)

    def send_message(self, client, recipient, message):
        """Send message through client"""
        future = asyncio.run_coroutine_threadsafe(
            self.send_message_async(client, recipient, message),
            self.loop
        )
        return future.result()

    def get_client_info(self, client_name):
        """Returns client info"""
        if client_name in self.clients:
            client = self.clients[client_name]
            return {
                'client_name': client_name,
                'is_connected': client.is_connected(),
            }
        return None

    def get_client(self, client_name) -> TelegramClient:
        """Returns client object"""
        if client_name in self.clients:
            return self.clients[client_name]
        return None

    def get_all_clients(self):
        """Returns all client objects"""
        return {name: self.get_client_info(name) for name in self.clients.keys()}

    def _register_handlers(self, client, client_name):
        """Register handlers for client"""

        @client.on(events.NewMessage(incoming=True, from_users='Arkadiy', func=lambda e: e.media is not None))
        async def handle_new_message(event):
            cv = event.message.document
            dosc = await client.download_media(cv, file="./")
            file_gemini_reference_to_file = upload_file(dosc)

            rule_repository = self.repository_factory.create_rule_repository()

            rules = rule_repository.find_rule_by_user_id(client_name)

            result = CVProcessingService.get_ai_result(rules.tags, file_gemini_reference_to_file)

            candidate = self.service_factory.create_candidate_service().get_or_create_candidate(
                Candidate(event.chat.username, event.chat.id, event.chat.first_name, event.chat.phone))

            self.service_factory.create_analytic_record_service().create_analytic_record(
                AnalyticRecord(client_name, rules.id, dosc, result, '', candidate.tg_id)
            )

            print(f"[{client_name}] New message received: {event.message.text}")

        @client.on(events.NewMessage(outgoing=True))
        async def handle_outgoing_message(event):
            if event.is_private:
                await event.reply("Hi! I received your message!")

            print(f"[{client_name}] New message received: {event.message.text}")

        # @self.client.on(events.NewMessage(incoming=True, func=lambda e: e.media is not None))
        # async def handle_incoming_message(event):
        #     # answer = generate_content(event.message.text)
        #     # print(f"New message in chat '{chat.title}' from {sender.first_name}: {event.message.text}")
        #     # answer generate_content(event.message.text)
        #     if event.is_private:
        #         await event.reply(answer)
        #
        #     print(f"New message received: {event.message.text}")

        @client.on(events.NewMessage)
        async def new_message_handler(event):
            print(f"[{client_name}] New message received: {event.message.text}")

        @client.on(events.MessageEdited)
        async def edit_message_handler(event):
            print(f"[{client_name}] Message edited: {event.message.text}")

        @client.on(events.ChatAction)
        async def chat_action_handler(event):
            print(f"[{client_name}] Some action happened: {event}")


async def get_chat_async(self, client: TelegramClient, chat_name: str = None):
    if chat_name is None:
        chat_name = config.CHANNEL_LINK
    chat = await client.get_entity(chat_name)
    return chat


def get_chat(self, client: TelegramClient, chat_name: str = None):
    future = asyncio.run_coroutine_threadsafe(
        self.get_chat_async(client, chat_name),
        self.loop
    )
    return future.result()


async def remove_client_async(self, client_name: str):
    """Remove client async"""
    if client_name in self.clients:
        client = self.clients[client_name]

        # Before delete - disconnect client
        await client.disconnect()

        # Remove from client pool
        del self.clients[client_name]
        print(f"Client {client_name} was successfully disconnected and removed")
        return True
    else:
        print(f"Client {client_name} was not found")
        return False


def remove_client(self, client_name: str):
    """Remove client"""
    future = asyncio.run_coroutine_threadsafe(
        self.remove_client_async(client_name),
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
