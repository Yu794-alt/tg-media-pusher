import uuid

from entities.user_entity import User


class UserRepository:

    def __init__(self, db_connection):
        self.db_connection = db_connection
        

    def create_user(self, login, password):
        connect = self.db_connection

        result = connect.execute("INSERT INTO users (login, password, salt) VALUES(?, ?, ?)",
                                 (login, password, str(uuid.uuid4())))
        connect.commit()
        new_user_id = result.lastrowid
        return new_user_id

    def find_user_by_id(self, id):
        connect = self.db_connection
        # use tuple even for single params
        cursor = connect.execute("SELECT * FROM users WHERE users.id = ?", (id,))
        row = cursor.fetchone()

        if row is None:
            return None

        return User(
            row['id'],
            row['login'],
            row['password'],
            row['salt'],
        )
