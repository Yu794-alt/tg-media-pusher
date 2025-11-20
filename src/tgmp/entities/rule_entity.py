from entities.user_entity import User


class Rule:
    def __init__(self, user: User, tags: str, date_start, date_end):
        self.id: int
        self.user: User = user
        self.tags: str = tags
        self.date_start: None | str = date_start
        self.date_end: None | str = date_end
