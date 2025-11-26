import uuid

from entities.user_entity import User


class UserRepository:

    def __init__(self, connect):
        self.connect = connect

    def create_user(self, login, password) -> int:
        connect = self.connect

        result = connect.execute("INSERT INTO users (login, password, salt) VALUES(?, ?, ?)",
                                 (login, password, str(uuid.uuid4())))
        connect.commit()
        new_user_id = result.lastrowid
        return new_user_id

    def find_user_by_id(self, id) -> User:
        connect = self.connect
        cursor = connect.execute("SELECT * FROM users WHERE users.id = ? ", (id,))
        row = cursor.fetchone()
        return User(
            row['id'],
            row['login'],
            row['password'],
            row['salt'],
        )

    def find_user_by_login(self, login) -> User:
        connect = self.connect
        cursor = connect.execute("SELECT * FROM users WHERE users.login = ? ", (login,))
        row = cursor.fetchone()
        cursor.close()

        if row is None:
            return None

        return User(
            row['id'],
            row['login'],
            row['password'],
            row['salt'],
        )
