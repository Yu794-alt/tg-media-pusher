from flask import Flask
from controllers.main_controller import main_bp

app = Flask(__name__)
app.register_blueprint(main_bp)

@app.after_request
def add_no_cache_headers(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

def main():
    app.run(debug=True)

if __name__ == "__main__":
    main()
