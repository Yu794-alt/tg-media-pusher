import uuid


class User:
    def __init__(self, id: int = None, login: str = None, password: str = None, salt: str | None = str(uuid.uuid4())):
        self.id = id
        self.login = login
        self.password = password
        self.salt = salt
