#from handlers import make_s_msg_obj, state
from storage import keyboards, users_storage, make_s_msg_obj, state


def handle(user_id):
    s_msg = "Дополнительные параметры"
    keyboard = keyboards['additional']
    users_storage[user_id]['state'] = state.INACTION
    s_msg_obj = make_s_msg_obj(s_msg=s_msg, keyboard=keyboard)
    return s_msg_obj