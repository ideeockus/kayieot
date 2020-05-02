from enum import Enum
import json

users_storage = {}
keyboards = {}

def addKeyboard(name, path):
        with open(path, 'r', encoding="utf-8") as keyboard: # чтение файла с объектом клавиатуры
            keyboards[name] = keyboard.read()

class state(Enum):
    WAIT_GROUP = "state_wait_for_group"
    START = "state_start"
    INACTION = "state_inaction"
    WAIT_PREPOD_NAME = "state_wait_for_prepod_name"

def make_s_msg_obj(s_msg, keyboard):
    s_msg_obj = { 's_msg': s_msg, 'keyboard':keyboard }
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
    with open("config.json", "r") as config_file:
        config = json.load(config_file)
        return config