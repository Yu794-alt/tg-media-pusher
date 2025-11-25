from repository.user_repository import UserRepository


class UserService:

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def create_user(self, login, password):
        return self.user_repository.create_user(login, password)

    def find_user_by_id(self, id):
        return self.user_repository.find_user_by_id(id)

    def find_user_by_login(self, login):
        return self.user_repository.find_user_by_login(login)
