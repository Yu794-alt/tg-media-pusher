from repository.user_repository import create_user


class UserService:

    @staticmethod
    def create_user(login, password):
        return create_user(login, password)