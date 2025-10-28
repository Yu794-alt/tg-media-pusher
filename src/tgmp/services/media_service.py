
# import asyncio
# from entities.media_entity import Media
# from services.messager_service import MessagerService
# from services.messager_telegram_service import TelegramMessager
# from services.telegram.impl.telegram_conncet_chanel import TelegramConnectChannel

# class MediaService:
#     def __init__(self):
#         self.messager = TelegramMessager(TelegramConnectChannel())
#         self.client = None
#         self.entity = None

#     async def init_connection(self):
#         """Ensure we have a client and entity before sending anything."""
#         if not self.client or not self.entity:
#             self.client, self.entity = await self.messager.connect()


