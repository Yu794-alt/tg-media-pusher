from .main import app
from .db import close_connection
from flask import Flask

app.teardown_appcontext(close_connection)