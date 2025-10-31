import asyncio
from flask import Blueprint

from services.telegram.impl.telegram_conncet_chanel import TelegramConnectChannel
from services.telegram_messager_service import TelegramMessagerService

main_bp = Blueprint('main', __name__)

tg_connection = TelegramConnectChannel()
ms = TelegramMessagerService(tg_connection)

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


@main_bp.route("/", methods=["GET"])
def index():    
    asyncio.run_coroutine_threadsafe(ms.send_message(), loop)
    return {"message": "Video folder retrieved successfully"}
