from flask import Blueprint, jsonify
from ..services.user_service import get_welcome_message

main_bp = Blueprint('main', __name__)

@main_bp.route("/", methods=["GET"])
def index():
    return jsonify(get_welcome_message())
