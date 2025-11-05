from abc import ABC, abstractmethod

class TelegramConnect(ABC):
    
    @abstractmethod
    async def connect(self):
        "Connecting to Telegram Channel..."