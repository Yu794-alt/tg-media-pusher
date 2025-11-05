import asyncio
from flask import Blueprint, render_template, current_app as app

main_bp = Blueprint('main', __name__)


# @main_bp.route("/", methods=["GET"])
# def index():
#     ms = app.config["TELEGRAM_MESSAGER_SERVICE"]
#     task = asyncio.run_coroutine_threadsafe(ms.client.send_message(ms.entity, 'bla bla'), ms.loop)
#     result = task.result()
#     return {"message": f"{result}"}
@main_bp.route("/", methods=["GET"])
def index():
    return render_template("main.html")
