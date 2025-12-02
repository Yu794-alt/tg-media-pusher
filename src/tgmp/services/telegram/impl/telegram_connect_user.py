from warnings import catch_warnings

from telethon import TelegramClient
from telethon.tl.functions.account import GetPasswordRequest
from telethon.sessions import StringSession

import config
from services.telegram.telegram_connect import TelegramConnect


class TelegramConnectUser(TelegramConnect):
    # client: TelegramClient | None = None

    def __init__(self, phone: str, string_session: str = None, session_name: str = None, auth_code: str = None, ):
        self.phone = phone
        self.string_session = string_session
        self.session_name = session_name
        self.auth_code = auth_code
        self.client = None
        self.password = None
        self.password_hint = None
        self.session = None
        self.is_connected = False

    async def connect(self, telethon=None):
        api_id = config.API_ID
        api_hash = config.API_HASH

        if self.client is None:

            if self.string_session:
                self.client = TelegramClient(StringSession(self.string_session), api_id, api_hash)
            elif self.session_name:
                self.client = TelegramClient(self.session_name, api_id, api_hash)
            else:
                raise ValueError(
                    "TelegramConnectUser was created improperly: it contains no session name or session string")

        await self.client.connect()
        self.is_connected = await self.client.is_user_authorized()
        if not self.is_connected:
            # await self.client.send_code_request(phone=self.phone)
            if not self.auth_code:
                await self.client.send_code_request(phone=self.phone)
                return

            try:
                if self.password is None:
                    await self.client.sign_in(phone=self.phone, code=self.auth_code)

                else:
                    await self.client.sign_in(password=self.password)
                    self.password = None
                    self.password_hint = None

            except (telethon.errors.SessionPasswordNeededError or telethon.errors.PasswordHashInvalidError):
                request_hint = await self.client(GetPasswordRequest())
                self.password_hint = request_hint.hint
                return

        self.is_connected = await self.client.is_user_authorized()