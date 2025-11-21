from entities.user_entity import User


class Rule:
    def __init__(self, user: User, tags: str, date_start: str = None, date_end: str = None, id: int = None):
        self.id: int = id
        self.user: User = user
        self.tags: str = tags
        self.date_start: str = date_start
        self.date_end: str = date_end
