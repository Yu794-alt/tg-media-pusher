# This file marks the directory as a Python package.
# It can also be used to run package initialization code if needed.

from .main import app
from .db import close_connection
from flask import Flask

app.teardown_appcontext(close_connection)