from multiprocessing import Manager
from typing import cast
from urllib import request
import json

from flask import Blueprint, render_template, request, jsonify, session, redirect, current_app as app
from flask_socketio import emit

from entities.rule_entity import Rule
from utils.helpers.socket_extensions import socketio

from entities.user_entity import User
from factories.service_factory import ServiceFactory
from services.telegram.impl.telegram_connect_user import TelegramConnectUser
from services.telegram_messager_service import TelegramMessagerService
from utils.helpers.get_telegram_client import get_telegram_connection, remove_telegram_connection

# tg_connections = Manager().dict()
tg_connections = {}
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
            if session['user_id']:
                user  = service_factory.create_user_service().find_user_by_id(session['user_id'])
                service_factory.create_rule_service().create_rule(Rule(user, tags=tags))
            else:
                raise Exception("No user found")

    return render_template("pages/configuration.html")


@main_bp.route("/howItworks", methods=["get"])
def howItworks():
    return render_template('pages/howItworks.html')


@main_bp.route("/signin", methods=["POST"])
def signin():
    username = request.form.get("login")
    password = request.form.get("password")

    service_factory = cast(ServiceFactory, app.config['SERVICE_FACTORY'])

    user = service_factory.create_user_service().find_user_by_login(username)

    if user is None:
        return render_template('pages/error.html', message="User not found")

    # UserService(UserRepository(app.config['db_connect'])).create_user(username, password)
    session["user_id"] = user.id
    # return jsonify({'message': 'successes',  'redirect1': '/'}), 200
    return redirect('/')


@main_bp.route("/signup", methods=["POST"])
def signup():
    # registration
    username = request.form.get("login")
    password = request.form.get("password")

    service_factory = cast(ServiceFactory, app.config['SERVICE_FACTORY'])

    user_id = service_factory.create_user_service().create_user(username, password)
    session["user_id"] = user_id
    # return jsonify({'message': 'successes',  'redirect1': '/'}), 200
    return redirect('/')


@main_bp.route("/dashboard", methods=["GET"])
def dashboard():
    user_id = session["user_id"]
    if user_id is None:
        return render_template("pages/error.html", message="User not found"'/')

    service_factory = cast(ServiceFactory, app.config['SERVICE_FACTORY'])

    rules = service_factory.create_rule_service().find_all_rules_by_user(User(id=user_id))
    last_rule = service_factory.create_rule_service().find_last_rule_by_user_id(user_id)
    analytic_records = service_factory.create_analytic_record_service().get_analytic_records_by_rule_id(user_id=user_id, rule_id=last_rule.id)

    # Parse ai_result and collect all unique technology columns
    tech_columns = []
    for record in analytic_records:
        try:
            ai_data = json.loads(record.ai_result) if isinstance(record.ai_result, str) else record.ai_result
            record.ai_result_parsed = ai_data
            # Collect all unique tech keys (preserve order of first appearance)
            for tech in ai_data.keys():
                if tech not in tech_columns:
                    tech_columns.append(tech)
        except (json.JSONDecodeError, AttributeError, TypeError):
            record.ai_result_parsed = {}

    return render_template('pages/dashboard.html', rules=rules, analytic_records=analytic_records,
                           tech_columns=tech_columns)


@main_bp.route("/technologies", methods=["POST"])
def technologies():
    service_factory = cast(ServiceFactory, app.config['SERVICE_FACTORY'])
    user_id = session["user_id"]

    data = request.get_json()
    rule_id = data if isinstance(data, (int, str)) else data.get('rule_id')

    if not rule_id:
        return jsonify({
            'success': False,
            'message': 'Rule ID is required'
        }), 400

    # Get filtered analytic records
    analytic_records = service_factory.create_analytic_record_service().get_analytic_records_by_rule_id(
        rule_id, user_id
    )

    # Parse ai_result and collect tech columns
    tech_columns = []
    records_data = []

    for record in analytic_records:
        try:
            ai_data = json.loads(record.ai_result) if isinstance(record.ai_result, str) else record.ai_result

            # Collect unique tech columns
            for tech in ai_data.keys():
                if tech not in tech_columns:
                    tech_columns.append(tech)

            # Prepare record data
            records_data.append({
                'user_id': record.user_id,
                'cv_path': record.cv_path,
                'rule_id': record.rule.id,
                'opinion': record.opinion,
                'ai_result': ai_data,
                'candidate_tg_id': record.candidate.tg_id if record.candidate else None
            })
        except (json.JSONDecodeError, AttributeError, TypeError):
            records_data.append({
                'user_id': record.user_id,
                'cv_path': record.cv_path,
                'rule_id': record.rule.id,
                'opinion': record.opinion,
                'ai_result': {},
                'candidate_tg_id': record.candidate.tg_id if record.candidate else None
            })

    return jsonify({
        'success': True,
        'records': records_data,
        'tech_columns': tech_columns
    })


@main_bp.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@main_bp.route("/newClient", methods=["POST"])
def new_client():
    user_id = session["user_id"]

    if request.method == "POST":
        data = request.get_json()
        tg_phone = data.get('phone', None)
        tg_code = data.get('tg_code', None)
        tg_password = data.get('tg_password', None)
        ms = cast(TelegramMessagerService, app.config['TELEGRAM_MESSAGER_SERVICE'])

        tg_connect = get_telegram_connection(user_id,
                                             TelegramConnectUser(phone=tg_phone, session_name=f"client_{user_id}"),
                                             tg_connections)

        if tg_password:
            tg_connect.password = tg_password

        if tg_code:
            tg_connect.auth_code = tg_code

        ms.telegram_connector(tg_connect)

        if tg_connect.is_connected:
            ms.add_client(tg_connect.client, user_id)
            remove_telegram_connection(user_id, tg_connections)

            return jsonify({
                'code': 4,
                'message': f'Client  was successfully connected'})

        if not tg_code:
            return jsonify({
                'code': 2,
                'error': 'You must provide request code we sent it to your device'})

        if tg_connect.password_hint:
            return jsonify({
                'code': 3,
                'error': f'You have enabled 2FA and you must provide password. Password hint: {tg_connect.password_hint}'})

    remove_telegram_connection(user_id, tg_connections)
    return jsonify({
        'code': 5,
        'error': f'Something went wrong. Please try again later.'})


@socketio.on("get_dashboard_row")
def get_dashboard_row():
    user_id = session["user_id"]

    service_factory = cast(ServiceFactory, app.config['SERVICE_FACTORY'])

    analytic_records = service_factory.create_analytic_record_service().get_last_analytic_record_by_user_id(user_id)

    # Parse ai_result JSON
    try:
        ai_result_parsed = json.loads(analytic_records.ai_result) if isinstance(analytic_records.ai_result,
                                                                                str) else analytic_records.ai_result
    except (json.JSONDecodeError, AttributeError, TypeError):
        ai_result_parsed = {}

    socketio.emit("new_analytic_record", {"user_id": analytic_records.user_id,
                                          "cv_path": analytic_records.cv_path,
                                          "rule_id": analytic_records.rule.id,
                                          "opinion": analytic_records.opinion,
                                          "ai_result": ai_result_parsed,
                                          "candidate_tg_id": analytic_records.candidate.tg_id
                                          })
