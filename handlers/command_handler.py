from . import additional_handler
from . import information_handler
import storage
from storage import make_s_msg_obj, users_storage, keyboards, state


def timetable(user_id):
    #timetable = getTimetable()
    #formated_timetable = formatTimetable(timetable)
    #return formated_timetable
    s_msg = "Хорошо, скажи свою группу"
    keyboard = keyboards['main']
    users_storage[user_id]['state'] = state.WAIT_GROUP
    return make_s_msg_obj(s_msg=s_msg, keyboard=keyboard)

def additional(user_id):
    """s_msg = "Дополнительные параметры пока в разработке"
    keyboard = keyboards['main']
    users_storage[user_id]['state'] = state.INACTION
    return make_s_msg_obj(s_msg, keyboard)"""
    s_msg_obj = additional_handler.handle(user_id)
    return s_msg_obj

def information(user_id):
    s_msg = information_handler.get_information()
    keyboard = keyboards['additional']
    users_storage[user_id]['state'] = state.INACTION
    return make_s_msg_obj(s_msg=s_msg, keyboard=keyboard)

def prepod_timetable(user_id):
    s_msg = "Введи имя преподавателя"
    keyboard = keyboards['main']
    users_storage[user_id]['state'] = state.WAIT_PREPOD_NAME
    return make_s_msg_obj(s_msg=s_msg, keyboard=keyboard)

def switch_timetable_output_mode(user_id):
    storage.timetable_output_mode = "image" if storage.timetable_output_mode=="text" else "text"
    s_msg = "Режим вывода расписания: "+ ("текст" if storage.timetable_output_mode=="text" else "картинка")
    keyboard = keyboards['additional']
    users_storage[user_id]['state'] = state.INACTION
    return make_s_msg_obj(s_msg=s_msg, keyboard=keyboard)

def home(user_id):
    s_msg = "Переключаю"
    keyboard = keyboards['main']
    users_storage[user_id]['state'] = state.INACTION
    return make_s_msg_obj(s_msg=s_msg, keyboard=keyboard)


commands = {
    'расписание': timetable,
    'дополнительно': additional,
    'info': information,
    'расписание преподователей': prepod_timetable,
    'изменить вывод расписания': switch_timetable_output_mode,
    'назад': home
    }



def handle(event):
    #vkapiserver = vkas
    user_id = event['object']['message']['from_id']
    r_msg = event['object']['message']['text']

    s_msg_obj = commands[r_msg](user_id)
    return s_msg_obj