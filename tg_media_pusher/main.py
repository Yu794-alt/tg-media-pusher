from flask import Flask
from .controllers.main_controller import main_bp

app = Flask(__name__)
app.register_blueprint(main_bp)

def main():
    app.run(debug=True)

if __name__ == "__main__":
    main()
