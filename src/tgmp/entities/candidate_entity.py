import uuid


class Candidate:
    def __init__(self, user_name: str, tg_id: str, name: str, phone: str):
        self.user_name: str = user_name
        self.tg_id: str = tg_id
        self.name: str = name
        self.phone: str = phone
