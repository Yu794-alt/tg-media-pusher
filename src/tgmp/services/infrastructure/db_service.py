import os
import sqlite3

import config

from flask import current_app as app


class DbService:

    @staticmethod
    def get_db_connection(connection_string):
        conn = sqlite3.connect(connection_string)
        conn.row_factory = sqlite3.Row  # Для доступа к колонкам по имени
        return conn