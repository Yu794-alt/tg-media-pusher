from abc import ABC, abstractmethod

class TelegramConnect(ABC):
    
    @abstractmethod
    async def connect(self):
        pass