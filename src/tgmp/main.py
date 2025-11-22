import os
import sqlite3

import config
from controllers.main_controller import main_bp
from flask import Flask
from flask_session import Session
from livereload import Server

from services.telegram.impl.telegram_connect_user import TelegramConnectUser
from services.telegram_messager_service import TelegramMessagerService

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


def get_db_connection():
    conn = sqlite3.connect(config.DATABASE)
    conn.row_factory = sqlite3.Row  # Для доступа к колонкам по имени
    return conn


def init_db():
    os.makedirs(app.instance_path, exist_ok=True)

    conn = get_db_connection()
    with app.open_resource(config.DB_SCHEMA) as f:
        conn.executescript(f.read().decode('utf8'))
    conn.close()


def run_services():
    tg_connection = TelegramConnectUser(config.PHONE,session_name="name")
    ms = TelegramMessagerService()
    ms.start()
    # Don't add multiple clients with same session file (sqlite3 databases)
    ms.add_client(tg_connection, 'client1')
    #ms.add_client(tg_connection, 'client2')
    app.config['TELEGRAM_MESSAGER_SERVICE'] = ms


def main():
    run_services()
    init_db()
    app.config['db_connect'] = get_db_connection()
    server.serve(port=5500, host="127.0.0.1", debug=False)
    # app.run(debug=False)


if __name__ == "__main__":
    server = Server(app.wsgi_app)
    server.watch(TEMPLATES_DIR)
    server.watch(STATIC_DIR)
    main()
