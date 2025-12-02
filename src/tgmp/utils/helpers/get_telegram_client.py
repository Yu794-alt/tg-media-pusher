def get_telegram_connection(user_id, tg, array):
    client_key = f"client_{user_id}"
    if client_key not in array:
        array[client_key] = tg
    return array[client_key]

def remove_telegram_connection(user_id, array):
    client_key = f"client_{user_id}"
    if client_key in array:
        array.pop(client_key)
