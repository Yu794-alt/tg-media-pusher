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


@main_bp.route("/signin", methods=["POST"])
def signin():
    username = request.form.get("login")
    password = request.form.get("password")

    service_factory = cast(ServiceFactory, app.config['SERVICE_FACTORY'])

    row_id = service_factory.create_user_service().find_user_by_login(username)

    if row_id is None:
        return render_template('pages/error.html', message="User not found")

    # UserService(UserRepository(app.config['db_connect'])).create_user(username, password)
    session["user_id"] = row_id
    # return jsonify({'message': 'successes',  'redirect1': '/'}), 200
    return redirect('/')


@main_bp.route("/signup", methods=["POST"])
def signup():
    # registration
    username = request.form.get("login")
    password = request.form.get("password")

    service_factory = cast(ServiceFactory, app.config['SERVICE_FACTORY'])

    row_id = service_factory.create_user_service().create_user(username, password)
    session["user_id"] = row_id
    # return jsonify({'message': 'successes',  'redirect1': '/'}), 200
    return redirect('/')

@main_bp.route("/dashboard", methods=["GET"])
def dashboard():
    user_id = session["user_id"]
    if user_id is None:
        return render_template("pages/error.html", message="User not found"'/')


    service_factory = cast(ServiceFactory, app.config['SERVICE_FACTORY'])

    # analytic_records = service_factory.create_analytic_record_service().(username, password)


    # return jsonify({'message': 'successes',  'redirect1': '/'}), 200
    return render_template('pages/dashboard.html', analytic_records=[])


@main_bp.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")
