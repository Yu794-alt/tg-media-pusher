from abc import ABC, abstractmethod

class TelegramConnect(ABC):
    
    @abstractmethod
    def connect(self):
        "Connecting to Telegram Channel..."