from ..repositories.user_repository import get_user_by_id
from ..db import get_db

def get_user(user_id: int):
    conn = get_db()
    return get_user_by_id(conn, user_id)

def get_welcome_message():
    return {"message": "Welcome from the user service!"}

