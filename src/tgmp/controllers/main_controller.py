import asyncio
from turtledemo.sorting_animate import enable_keys
from urllib import request

from flask import Blueprint, render_template, jsonify, request, session, redirect, current_app as app
from werkzeug.wrappers import Response as BaseResponseBlaBla

from entities.rule_entity import Rule
from services.user_service import UserService

main_bp = Blueprint('main', __name__)


# @main_bp.route("/", methods=["GET"])
# def index():
#     ms = app.config["TELEGRAM_MESSAGER_SERVICE"]
#     task = asyncio.run_coroutine_threadsafe(ms.client.send_message(ms.entity, 'bla bla'), ms.loop)
#     result = task.result()
#     return {"message": f"{result}"}
@main_bp.route("/", methods=["GET"])
def index():
    return render_template("pages/main.html")


@main_bp.route("/config", methods=["GET", "POST"])
def config():
    if request.method == "POST":
        data = request.get_json()

        if data:
            tags = data.get('tags', [])
            print(session['user_id'])
            if session['user_id']:
                user = UserService.find_user_by_id(session['user_id'])
                Rule(user, tags)
            else:
                raise Exception("No user found")

    return render_template("pages/configuration.html")


@main_bp.route("/signup", methods=["POST"])
def signup():
    username = request.form.get("login")
    password = request.form.get("password")
    row_id = UserService.create_user(username, password)
    session["user_id"] = row_id
    # return jsonify({'message': 'successes',  'redirect1': '/'}), 200
    return redirect('/')
