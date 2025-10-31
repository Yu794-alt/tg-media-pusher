from controllers.main_controller import ms, loop, main_bp
import threading
from flask import Flask

app = Flask(__name__)
app.register_blueprint(main_bp)

@app.after_request
def add_no_cache_headers(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

async def run_bot():
    try:
        await ms.connect()
        await ms.setup_handlers()
        await ms.client.run_until_disconnected()
    except Exception as e:
        print(f"Bot error: {e}")


def main():
    threading.Thread(target=lambda: loop.run_until_complete(run_bot()), daemon=True).start()
    app.run(debug=True)

if __name__ == "__main__":    
    main()
