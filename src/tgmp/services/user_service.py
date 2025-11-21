from repository.user_repository import  UserRepository


class UserService:

    @staticmethod
    def create_user(login, password):
        return UserRepository.create_user(login, password)

    @staticmethod
    def find_user_by_id(id):
        return UserRepository.find_user_by_id(id)
