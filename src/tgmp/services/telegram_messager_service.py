import asyncio
import threading

from api.gemini import generate_content
from entities.media_entity import Media
from telethon import events

from services.messager_service import MessagerService
from services.telegram.telegram_connect import TelegramConnect

class TelegramMessagerService(MessagerService):

    def __init__(self, con: TelegramConnect):
        self.tgConnect = con
        self.client = None
        self.entity = None

    async def setup_handlers(self):
        @self.client.on(events.NewMessage(incoming=True, from_users='Arkadiy', func=lambda e: e.media is None))
        async def handle_new_message(event):
            answer = generate_content(event.message.text)
            if event.is_private and not event.out:
                await event.reply(answer)

            print(f"New message received: {event.message.text}")

        @self.client.on(events.NewMessage(outgoing=True))
        async def handle_outgoing_message(event):
            if event.is_private:
                await event.reply("Привет! Я получил твое сообщение!")

            print(f"New message received: {event.message.text}")

        @self.client.on(events.NewMessage(incoming=True, func=lambda e: e.media is not None))
        async def handle_incoming_message(event):
            answer = generate_content(event.message.text)
            # print(f"Новое сообщение в чате '{chat.title}' от {sender.first_name}: {event.message.text}")
            # answer generate_content(event.message.text)
            if event.is_private:
                await event.reply(answer)

            print(f"New message received: {event.message.text}")

    # async def setup_handlers(self):
    #     @self.client.on(events.NewMessage(incoming=True))
    #     async def handle_new_dosc(event):
    #         sender = await event.get_sender()
    #         chat = await event.get_chat()
    #
    #         # print(f"Новое сообщение в чате '{chat.title}' от {sender.first_name}: {event.message.text}")
    #         # answer generate_content(event.message.text)
    #         if event.is_private and not event.out:
    #             await event.reply("Привет! Я получил твое сообщение!")
    #
    #         print(f"New message received: {event.message.text}")

    async def send_video(self):
        folder = Media("D:\\tv", extensions=[".mp4", ".webm", ".avi"])
        videos = folder.get_media_files()

        for video in videos:
            await  self.client.send_file(self.entity, video)
            print(f"Отправлено: {video}")

        return {"message": "Video folder retrieved successfully"}

    async def send_message(self):
        await self.client.send_message(self.entity, "Hello, Channel! entity")
        return {"message": "Message sent successfully"}

    def upload_files(self, files):
        for file in files:
            print(f"Uploading {file} to Telegram...")

    async def connect(self):
        self.client, self.entity = await self.tgConnect.connect()

    async def _start_thread(self):
        # try:
        await self.connect()
        await self.setup_handlers()
        await self.client.run_until_disconnected()
        # except Exception as e:
        #     print(f"Bot error: {e}")

    def create_new_thread(self):
        def new_thread():
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            self.loop.run_until_complete(self._start_thread())


        threading.Thread(target=new_thread, daemon=True).start()
