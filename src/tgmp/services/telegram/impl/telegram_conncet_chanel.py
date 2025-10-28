import os
from services.telegram.telegram_connect import TelegramConnect
from telethon import TelegramClient
# from config import API_ID, API_HASH, CHANNEL_LINK
import config

class  TelegramConnectChannel(TelegramConnect):
        
    async def connect(self):
        api_id = config.API_ID
        api_hash = config.API_HASH
        phone = config.PHONE
        channel_link = config.CHANNEL_LINK
        client = TelegramClient('name', api_id, api_hash)
        await  client.start(phone)
        
        entity =  await  client.get_entity(channel_link)
        # async for message in client.iter_messages(channel_link):
        #     print(f"{message.date}: {message.sender_id} - {message.text}")

        return client, entity       
    

