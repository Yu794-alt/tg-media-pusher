from telethon import TelegramClient
from telethon.sessions import StringSession

import config
from services.telegram.telegram_connect import TelegramConnect

class  TelegramConnectUser(TelegramConnect):
    def __init__(self, phone : str, string_session : str = None, session_name : str = None):
        self.phone = phone
        self.string_session = string_session
        self.session_name = session_name


        
    async def connect(self):
        api_id = config.API_ID
        api_hash = config.API_HASH

        if self.string_session:
            client = TelegramClient(StringSession(self.string_session), api_id, api_hash)
        elif self.session_name:
            client = TelegramClient(self.session_name, api_id, api_hash)
        else:
            raise ValueError("TelegramConnectUser was created improperly: it contains no session name or session string")

        await client.start(self.phone)

        return client
    

