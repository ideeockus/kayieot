#from handlers import make_s_msg_obj, state
from storage import keyboards, users_storage, make_s_msg_obj, state


def handle(user_id):
    msg = "Дополнительные параметры"
    keyboard = keyboards['additional']
    users_storage[user_id]['state'] = state.INACTION
    s_msg_obj = make_s_msg_obj(msg, keyboard)
    return s_msg_obj