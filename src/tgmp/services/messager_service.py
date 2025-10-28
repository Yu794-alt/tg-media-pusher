from abc import ABC, abstractmethod

class MessagerService(ABC):

    @abstractmethod
    def upload_files(self, files):
        self.messenger_impl.upload_files(files)

    @abstractmethod
    def connect(self):
        self.messenger_impl.connect()

    