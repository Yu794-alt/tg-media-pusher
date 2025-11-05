import os

from controllers.main_controller import main_bp
from flask import Flask
from livereload import Server

from services.telegram.impl.telegram_conncet_chanel import TelegramConnectChannel
from services.telegram_messager_service import TelegramMessagerService

base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

TEMPLATES_DIR = os.path.join(base_dir, 'frontend/templates')
STATIC_DIR = os.path.join(base_dir, 'frontend/static')
app = Flask(__name__,
            template_folder=TEMPLATES_DIR,
            static_folder=STATIC_DIR)

print(STATIC_DIR)
print(TEMPLATES_DIR)
print(base_dir)

app.register_blueprint(main_bp)

@app.after_request
def add_no_cache_headers(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

def run_services():
    tg_connection = TelegramConnectChannel()
    ms = TelegramMessagerService(tg_connection)
    ms.create_new_thread()
    app.config['TELEGRAM_MESSAGER_SERVICE'] = ms


def main():
    run_services()
    server.serve(port=5500, host="127.0.0.1", debug=False)
    # app.run(debug=False)

if __name__ == "__main__":
    server = Server(app.wsgi_app)
    server.watch(TEMPLATES_DIR)
    server.watch(STATIC_DIR)
    main()
