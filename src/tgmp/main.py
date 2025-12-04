import os
import sqlite3

import config
from controllers.main_controller import main_bp
from flask import Flask
from flask_session import Session
from flask_socketio import SocketIO
from livereload import Server

from factories.repository_factory import RepositoryFactory
from factories.service_factory import ServiceFactory
from services.telegram.impl.telegram_connect_user import TelegramConnectUser
from services.telegram_messager_service import TelegramMessagerService
from utils.helpers.db_connection_helper import DBConnection
from utils.helpers.socket_extensions import socketio

base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

TEMPLATES_DIR = os.path.join(base_dir, 'frontend/templates')
STATIC_DIR = os.path.join(base_dir, 'frontend/static')
app = Flask(__name__,
            template_folder=TEMPLATES_DIR,
            static_folder=STATIC_DIR)

app.config['DEBUG'] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.register_blueprint(main_bp)

Session(app)


@app.after_request
def add_no_cache_headers(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


def init_db():
    os.makedirs(app.instance_path, exist_ok=True)

    conn = DBConnection.get_SQL3_connection(config.DATABASE)
    with app.open_resource(config.DB_SCHEMA) as f:
        conn.executescript(f.read().decode('utf8'))
    conn.close()


def init_tg_messagers_service():
    tg_connection = TelegramConnectUser(config.PHONE, session_name="name")
    ms = TelegramMessagerService(app)
    ms.start()
    ms.telegram_connector(tg_connection)
    # Don't add multiple clients with same session file (sqlite3 databases)
    ms.add_client(tg_connection.client, '96')
    app.config['TELEGRAM_MESSAGER_SERVICE'] = ms


def init_factories():
    conn = DBConnection.get_SQL3_connection(config.DATABASE)
    repository_factory = RepositoryFactory(conn)
    service_factory = ServiceFactory(repository_factory)
    app.config['SERVICE_FACTORY'] = service_factory
    app.config['REPOSITORY_FACTORY'] = repository_factory


def main():
    init_db()
    init_factories()
    init_tg_messagers_service()
    socketio.init_app(app)
    socketio.run(app, port=5500, host="127.0.0.1", debug=False, allow_unsafe_werkzeug=True)


if __name__ == "__main__":
    # server = Server(app.wsgi_app)
    # server.watch(TEMPLATES_DIR)
    # server.watch(STATIC_DIR)
    main()
