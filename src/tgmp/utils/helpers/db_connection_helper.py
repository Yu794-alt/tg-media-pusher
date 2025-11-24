import sqlite3


class DBConnection:

    @staticmethod
    def get_SQL3_connection(database):
        conn = sqlite3.connect(database)
        conn.row_factory = sqlite3.Row
        return conn
