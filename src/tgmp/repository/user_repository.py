import uuid

from flask import current_app as app


def create_user(login, password):
    connect = app.config["db_connect"]

    result = connect.execute("INSERT INTO users (login, password, salt) VALUES(?, ?, ?)",
                    (login, password, str(uuid.uuid4())))
    connect.commit()
    new_user_id = result.lastrowid
    return new_user_id
