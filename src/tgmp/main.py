import os

import config
from controllers.main_controller import main_bp
from flask import Flask
from flask_session import Session
from livereload import Server

from factories.repository_factory import RepositoryFactory
from factories.service_factory import ServiceFactory
from services.infrastructure.db_service import DbService
from services.infrastructure.telegram.impl.telegram_connect_user import TelegramConnectUser
from services.infrastructure.telegram.telegram_messager_service import TelegramMessagerService

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
    conn = DbService.get_db_connection(config.DATABASE)
    with app.open_resource(config.DB_SCHEMA) as f:
        conn.executescript(f.read().decode('utf8'))
    conn.close()

def run_services():
    tg_connection = TelegramConnectUser(config.PHONE,session_name="name")
    ms = TelegramMessagerService()
    ms.start()
    # Don't add multiple clients with same session file (sqlite3 databases)
    # user_id = 1 is administrator client (for testing purposes)
    ms.add_client(tg_connection, 1)
    app.config['TELEGRAM_MESSAGER_SERVICE'] = ms
    #create factories
    repo_factory = RepositoryFactory(config.DATABASE)
    app.config['REPOSITORY_FACTORY'] = repo_factory
    service_factory = ServiceFactory(repo_factory)
    app.config['SERVICE_FACTORY'] = service_factory


def main():
    run_services()
    # create tables and schemas in database
    init_db()
    app.config['db_connect'] = DbService.get_db_connection(config.DATABASE)
    server.serve(port=5500, host="127.0.0.1", debug=False)
    # app.run(debug=False)


if __name__ == "__main__":
    server = Server(app.wsgi_app)
    server.watch(TEMPLATES_DIR)
    server.watch(STATIC_DIR)
    main()
