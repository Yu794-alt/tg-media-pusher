from entities.media_entity import Media
from telethon import  events

from services.messager_service import MessagerService
from services.telegram.telegram_connect import TelegramConnect



class TelegramMessagerService(MessagerService):
    def __init__(self, con: TelegramConnect):
        self.tgConnect = con
        self.client = None
        self.entity = None

    async def setup_handlers(self):
        @self.client.on(events.NewMessage(incoming=True))
        async def handle_new_message(event):
            sender = await event.get_sender()
            chat = await event.get_chat()
            print(event)
            log('log')
            # print(f"Новое сообщение в чате '{chat.title}' от {sender.first_name}: {event.message.text}")
            # answer generate_content(event.message.text)
            if event.is_private and not event.out:
                await event.reply("Привет! Я получил твое сообщение!")

            print(f"New message received: {event.message.text}")

        # @self.client.on(events.NewMessage(incoming=True))
        # async def handle_new_message(event):
        #     sender = await event.get_sender()
        #     chat = await event.get_chat()

        #     # print(f"Новое сообщение в чате '{chat.title}' от {sender.first_name}: {event.message.text}")
        #     # answer generate_content(event.message.text)
        #     if event.is_private and not event.out:
        #         await event.reply("Привет! Я получил твое сообщение!")

        #     print(f"New message received: {event.message.text}")


    
    async def setup_handlers(self):
        @self.client.on(events.NewMessage(incoming=True))
        async def handle_new_dosc(event):
            sender = await event.get_sender()
            chat = await event.get_chat()

            # print(f"Новое сообщение в чате '{chat.title}' от {sender.first_name}: {event.message.text}")
            # answer generate_content(event.message.text)
            if event.is_private and not event.out:
                await event.reply("Привет! Я получил твое сообщение!")

            print(f"New message received: {event.message.text}")

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
        
    