from . import timetable_handler
from . import prepod_timetable_handler
from . import command_handler
from storage import users_storage, keyboards, make_s_msg_obj, state
import logging
#from enum import Enum


logging.basicConfig(filename="handlers.log", level=logging.DEBUG) # лог для обработчиков

def handle(event):
    user_id = event['object']['message']['from_id']
    r_msg = event['object']['message']['text'] # received message

    if(not (user_id in users_storage)): # новый пользователь
        users_storage[user_id] = {}
        users_storage[user_id]['state'] = state.INACTION
        #s_msg = "Жми на кнопки" 
        #keyboard = keyboards['main']
        print("new user| inactive status")
        logging.info("new user| inactive status")
        #return make_s_msg_obj(s_msg, keyboard)


    if(r_msg in command_handler.commands):
        s_msg_obj = command_handler.handle(event)
        return s_msg_obj


    if(users_storage[user_id]['state']==state.WAIT_GROUP): # 
        print("user stat is wait for group")
        if(len(r_msg)>150): # лишком длинное сообщение
            s_msg = "Напиши покороче, пожалуйста"
            keyboard = keyboards['main']
            return make_s_msg_obj(s_msg, keyboard)
        s_msg_obj = timetable_handler.handle(event)
        return s_msg_obj


    if(users_storage[user_id]['state']==state.WAIT_PREPOD_NAME): # 
        print("user stat is wait for prepod name")
        if(len(r_msg)>150): # cлишком длинное сообщение
            s_msg = "Напиши покороче, пожалуйста"
            keyboard = keyboards['main']
            return make_s_msg_obj(s_msg, keyboard)
        s_msg_obj = prepod_timetable_handler.handle(event)
        return s_msg_obj




    s_msg = "что ты от меня хочешь?"
    keyboard = keyboards['main']
    users_storage[user_id]['state'] = state.INACTION
    return make_s_msg_obj(s_msg, keyboard)


