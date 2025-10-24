import sqlite3

def get_user_by_id(conn: sqlite3.Connection, user_id: int):
    cursor = conn.execute("SELECT id, username FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    if row:
        return {"id": row[0], "username": row[1]}
    return None
