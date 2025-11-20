import uuid

class User:
    def __init__(self, login: str, password: str):
        self.id = int
        self.login = login
        self.password = password
        self.salt =  uuid.uuid4()


