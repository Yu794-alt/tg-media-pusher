from flask import Blueprint, jsonify

from services.media_service import get_video

main_bp = Blueprint('main', __name__)

@main_bp.route("/", methods=["GET"])
def index():
    return get_video()
