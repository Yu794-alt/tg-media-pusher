import sqlite3

sqlite3.threadsafety = 3


class DBConnection:

    @staticmethod
    def get_SQL3_connection(database):
        conn = sqlite3.connect(database, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn
