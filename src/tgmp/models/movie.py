import sqlite3

class Movie:
    @staticmethod
    def create_table(conn: sqlite3.Connection):
        conn.execute("""
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            year INTEGER
        )
        """)
