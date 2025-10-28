from services.messager_service import MessagerService
from services.telegram.telegram_connect import TelegramConnect
from telethon import TelegramClient, events
from entities.media_entity import Media

class TelegramMessagerService(MessagerService):
    def __init__(self, con: TelegramConnect):
        self.tgConnect = con

    async def setup_handlers(self):
        await self.connect()
        @self.tgConnect.client.on(events.NewMessage(incoming=True))
        async def handle_new_message(event):
            sender = await event.get_sender()
            chat = await event.get_chat()

            # print(f"Новое сообщение в чате '{chat.title}' от {sender.first_name}: {event.message.text}")

            # Автоответчик
            if event.is_private and not event.out:
                await event.reply("Привет! Я получил твое сообщение!")

            print(f"New message received: {event.message.text}")
        await self.tgConnect.client.run_until_disconnected()

    async def send_video(self):
        await self.connect()
        folder = Media("D:\\tv", extensions=[".mp4", ".webm", ".avi"])
        videos = folder.get_media_files()

        for video in videos:
            await  self.tgConnect.client.send_file(self.tgConnect.entity, video)
            print(f"Отправлено: {video}")

        return {"message": "Video folder retrieved successfully"}

    async def send_message(self):
        await self.connect()
        await self.tgConnect.client.send_message(self.tgConnect.entity, "Hello, Channel! entity")
        return {"message": "Message sent successfully"}

    def upload_files(self, files):
        for file in files:
            print(f"Uploading {file} to Telegram...")

    async def connect(self):
        if getattr(self.tgConnect, "client", None) and getattr(self.tgConnect, "entity", None):
            return self.tgConnect.client, self.tgConnect.entity
        self.tgConnect.client, self.tgConnect.entity = await self.tgConnect.connect()
        return self.tgConnect.client, self.tgConnect.entity
        
    