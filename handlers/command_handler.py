from . import additional_handler
from . import information_handler
from storage import make_s_msg_obj, users_storage, keyboards, state


def timetable(user_id):
    #timetable = getTimetable()
    #formated_timetable = formatTimetable(timetable)
    #return formated_timetable
    s_msg = "Хорошо, скажи свою группу"
    keyboard = keyboards['empty']
    users_storage[user_id]['state'] = state.WAIT_GROUP
    return make_s_msg_obj(s_msg, keyboard)

def additional(user_id):
    """s_msg = "Дополнительные параметры пока в разработке"
    keyboard = keyboards['main']
    users_storage[user_id]['state'] = state.INACTION
    return make_s_msg_obj(s_msg, keyboard)"""
    s_msg_obj = additional_handler.handle(user_id)
    return s_msg_obj

def information(user_id):
    s_msg = information_handler.get_information()
    keyboard = keyboards['main']
    users_storage[user_id]['state'] = state.INACTION
    return make_s_msg_obj(s_msg, keyboard)

def prepod_timetable(user_id):
    s_msg = "Напиши имя"
    keyboard = keyboards['main']
    users_storage[user_id]['state'] = state.WAIT_PREPOD_NAME
    return make_s_msg_obj(s_msg, keyboard)


commands = {
    'Расписание': timetable,
    'дополнительно': additional,
    'info': information,
    'Расписание преподователей': prepod_timetable
    }



def handle(event):
    #vkapiserver = vkas
    user_id = event['object']['message']['from_id']
    r_msg = event['object']['message']['text']

    s_msg_obj = commands[r_msg](user_id)
    return s_msg_obj