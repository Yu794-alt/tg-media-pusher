import asyncio
from flask import Blueprint, jsonify

# from services.media_service import MediaService
# from api.gemini import generate_content
from services.telegram_messager_service import TelegramMessagerService
from services.telegram.impl.telegram_conncet_chanel import TelegramConnectChannel

main_bp = Blueprint('main', __name__)

@main_bp.route("/", methods=["GET"])
def index():
    # generate_content()
    ms = TelegramMessagerService(TelegramConnectChannel())
    # asyncio.run(ms.send_message())
    asyncio.run(ms.setup_handlers())
    return {"message": "Video folder retrieved successfully"}
