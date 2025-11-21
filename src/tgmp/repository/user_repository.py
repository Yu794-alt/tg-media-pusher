import uuid

from flask import current_app as app

from entities.user_entity import User


class UserRepository:

    @staticmethod
    def create_user(login, password):
        connect = app.config["db_connect"]

        result = connect.execute("INSERT INTO users (login, password, salt) VALUES(?, ?, ?)",
                                 (login, password, str(uuid.uuid4())))
        connect.commit()
        new_user_id = result.lastrowid
        return new_user_id

    @staticmethod
    def find_user_by_id(id):
        connect = app.config["db_connect"]
        row = connect.execute("SELECT * FROM users WHERE users.id = ? ", id)
        return User(
            row['id'],
            row['login'],
            row['password'],
            row['salt'],
        )
