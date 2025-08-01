import sqlite3

class User:
    @staticmethod
    def create_table(conn: sqlite3.Connection):
        conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE
        )
        """)
