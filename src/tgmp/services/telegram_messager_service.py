import asyncio
import threading
import uuid

import config
from api.gemini import generate_content, upload_file
from telethon import events, TelegramClient

from services.telegram.telegram_connect import TelegramConnect
from services.cv_processing_service import CVProcessingService

class TelegramMessagerService:

    def __init__(self):
        self.clients = {}
        self.loop = None
        self.thread = None
        self.is_running = False

    def _start_async_loop(self):
        """Start asyncio loop in new thread"""
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

    async def add_client_async(self, telegram_connect: TelegramConnect, client_name: str = None):
        """Add client asynchronously"""

        client = await telegram_connect.connect()

        if client_name is None:
            client_name = str(uuid.uuid4())
        # Регистрируем обработчики событий
        self._register_handlers(client, client_name)

        self.clients[client_name] = client
        print(f"Клиент {client_name} успешно запущен")

        return client

    def add_client(self, telegram_connect: TelegramConnect, client_name: str = None):
        """Add client"""
        future = asyncio.run_coroutine_threadsafe(
            self.add_client_async(telegram_connect, client_name),
            self.loop
        )
        return future.result()

    async def send_message_async(self, client, recipient, message):
        """Отправляет сообщение через указанного клиента"""
        await client.send_message(recipient, message)

    def send_message(self, client, recipient, message):
        """Отправляет сообщение (потокобезопасно)"""
        future = asyncio.run_coroutine_threadsafe(
            self.send_message_async(client, recipient, message),
            self.loop
        )
        return future.result()

    def get_client_info(self, client_name):
        """Возвращает информацию о клиенте"""
        if client_name in self.clients:
            client = self.clients[client_name]
            return {
                'client_name': client_name,
                'is_connected': client.is_connected(),
            }
        return None

    def get_client(self, client_name) -> TelegramClient:
        """Возвращает информацию о клиенте"""
        if client_name in self.clients:
            return  self.clients[client_name]
        return None

    def get_all_clients(self):
        """Возвращает информацию обо всех клиентах"""
        return {name: self.get_client_info(name) for name in self.clients.keys()}


    def _register_handlers(self, client, client_name):
        """Регистрирует обработчики событий для клиента"""

        @client.on(events.NewMessage(incoming=True, from_users='Arkadiy', func=lambda e: e.media is not None))
        async def handle_new_message(event):
            cv = event.message.document
            dosc = await client.download_media(cv, file="./")
            # file = os.path.basename()
            file_gemini_reference_to_file = upload_file(dosc)
            tags_from_bd = "javascript, react, laravel"
            result = CVProcessingService.get_ai_result(tags_from_bd, file_gemini_reference_to_file)
            print(result)
            # answer = generate_content(event.message.text)
            # if event.is_private and not event.out:
            #     await event.reply(answer)

            print(f"[{client_name}] New message received: {event.message.text}")

        @client.on(events.NewMessage(outgoing=True))
        async def handle_outgoing_message(event):
            if event.is_private:
                await event.reply("Привет! Я получил твое сообщение!")

            print(f"[{client_name}] New message received: {event.message.text}")

        # @self.client.on(events.NewMessage(incoming=True, func=lambda e: e.media is not None))
        # async def handle_incoming_message(event):
        #     # answer = generate_content(event.message.text)
        #     # print(f"Новое сообщение в чате '{chat.title}' от {sender.first_name}: {event.message.text}")
        #     # answer generate_content(event.message.text)
        #     if event.is_private:
        #         await event.reply(answer)
        #
        #     print(f"New message received: {event.message.text}")

        @client.on(events.NewMessage)
        async def new_message_handler(event):
            print(f"[{client_name}] Новое сообщение: {event.message.text}")
            # Здесь можно обрабатывать сообщения
            # Например, сохранять в базу, отправлять уведомления и т.д.

        @client.on(events.MessageEdited)
        async def edit_message_handler(event):
            print(f"[{client_name}] Сообщение отредактировано: {event.message.text}")

        @client.on(events.ChatAction)
        async def chat_action_handler(event):
            print(f"[{client_name}] Действие в чате: {event}")


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

    async def remove_client_async(self, client_name: str):
        """Удаляет клиент асинхронно"""
        if client_name in self.clients:
            client = self.clients[client_name]

            # Останавливаем клиента
            await client.disconnect()

            # Удаляем из пула клиентов
            del self.clients[client_name]
            print(f"Клиент {client_name} успешно остановлен и удален")
            return True
        else:
            print(f"Клиент {client_name} не найден")
            return False

    def remove_client(self, client_name: str):
        """Удаляет клиент (потокобезопасно)"""
        future = asyncio.run_coroutine_threadsafe(
            self.remove_client_async(client_name),
            self.loop
        )
        return future.result()
# # ПОКА НЕ ТРОГАТЬ СНИЗУ
#     async def send_video(self):
#         folder = Media("D:\\tv", extensions=[".mp4", ".webm", ".avi"])
#         videos = folder.get_media_files()
#
#         for video in videos:
#             await  self.client.send_file(self.entity, video)
#             print(f"Отправлено: {video}")
#
#         return {"message": "Video folder retrieved successfully"}
#
#     async def send_message(self):
#         await self.client.send_message(self.entity, "Hello, Channel! entity")
#         return {"message": "Message sent successfully"}
#
#     def upload_files(self, files):
#         for file in files:
#             print(f"Uploading {file} to Telegram...")