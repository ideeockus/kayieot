from enum import Enum
import json
import os

users_storage = {}
keyboards = {}
timetable_output_mode = "text"

def addKeyboard(name, path):
        with open(path, 'r', encoding="utf-8") as keyboard: # чтение файла с объектом клавиатуры
            keyboards[name] = keyboard.read()

class state(Enum):
    WAIT_GROUP = "state_wait_for_group"
    START = "state_start"
    INACTION = "state_inaction"
    WAIT_PREPOD_NAME = "state_wait_for_prepod_name"
    WAIT_GROUP_FOR_EXAMS = "state_wait_for_group_for_exams"
    WAIT_PREPOD_NAME_FOR_EXAMS = "state_wait_for_prepod_name_for_exams"

"""def make_s_msg_obj(s_msg, keyboard):
    s_msg_obj = { 's_msg': s_msg, 'keyboard':keyboard }
    #print(s_msg_obj)
    return s_msg_obj"""
def make_s_msg_obj(**kwargs): # обычно s_msg и keyboard
    s_msg_obj = {}
    for key, value in kwargs.items():
        if(key=="s_msg"): key = "message"
        s_msg_obj[key] = value
    #s_msg_obj = { 's_msg': s_msg, 'keyboard':keyboard }
    #print(s_msg_obj)
    return s_msg_obj

def saveStorage():
    with open("users_storage.json", "w") as users_storage_file:
        print(users_storage)
        json.dump(users_storage, users_storage_file)
       

def loadStorage():
    with open("users_storage.json", "r") as users_storage_file:
        try:
            users_storage = json.load(users_storage_file)
        except json.decoder.JSONDecodeError: #файл только создан
            pass

def getConfig():
    try:
        vk_key = os.environ.get('VK_KEY')
        group_id = os.environ.get('GROUP_ID')
        if(vk_key==None or group_id==None): raise KeyError
        config = {'VK_KEY': vk_key, 'GROUP_ID': group_id}
        print(config)
        return config
    except KeyError:
        print("os environments VK_KEY, GROUP_ID UNFOUND")
    with open("config.json", "r") as config_file:
        config = json.load(config_file)
        return config