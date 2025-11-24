from typing import cast
from urllib import request

from flask import Blueprint, render_template, request, session, redirect, current_app as app

from factories.service_factory import ServiceFactory

main_bp = Blueprint('main', __name__)

# @main_bp.route("/testMessage", methods=["GET"])
# def indexx():
#     # cast only for IDE IntelliCode
#     ms = cast(TelegramMessagerService,app.config["TELEGRAM_MESSAGER_SERVICE"])
#     client = ms.get_client(str(session['user_id']))
#     ms.send_message(session['user_id'],'me','hello channel')
#     return {"message": f"{ms.get_all_clients()}"}

@main_bp.route("/", methods=["GET"])
def index():
    return render_template("pages/main.html")


@main_bp.route("/config", methods=["GET", "POST"])
def config():
    if request.method == "POST":
        data = request.get_json()

        service_factory = cast(ServiceFactory, app.config['SERVICE_FACTORY'])

        if data:
            tags = data.get('tags', [])
            print(session['user_id'])
            if session['user_id']:
                # user_service = ServiceFactory().create_user_service(session['user_id'])
                service_factory.create_user_service().find_user_by_id(session['user_id'])
                # ms = cast(TelegramMessagerService,app.config["TELEGRAM_MESSAGER_SERVICE"])
                # client = ms.get_client(str(session['user_id']))
            else:
                raise Exception("No user found")

    return render_template("pages/configuration.html")


@main_bp.route("/signup", methods=["POST"])
def signup():
    username = request.form.get("login")
    password = request.form.get("password")

    service_factory = cast(ServiceFactory, app.config['SERVICE_FACTORY'])

    row_id = service_factory.create_user_service().create_user(username, password)
    # UserService(UserRepository(app.config['db_connect'])).create_user(username, password)
    session["user_id"] = '96'
    # return jsonify({'message': 'successes',  'redirect1': '/'}), 200
    return redirect('/')
