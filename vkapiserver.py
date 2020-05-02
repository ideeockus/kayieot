import requests
import json
import logging

#https://api.vk.com/method/METHOD_NAME?PARAMETERS&access_token=ACCESS_TOKEN&v=V 

logging.basicConfig(filename="vkApiServer.log", level=logging.DEBUG)
logging.info("loaded")
 

class vkApiServer:
    keyboard = {} # для хранения клавиатур
    def __init__(self, group_id, group_key, api_version=5.103):
        api_url = "https://api.vk.com/method/" # url для обращения к API
        r = requests.post(api_url+"groups.getLongPollServer", {'group_id':group_id, 'access_token': group_key, 'v': api_version}) # данные сессии
        response = r.json()
        logging.debug(response) # дебагаем
        if('error' in response):
            raise VkApiServerResponseError(response)
            #return
        

        self.vk_key = response['response']['key']
        self.server = response['response']['server']
        self.ts = response['response']['ts']
        self.group_id = group_id
        self.group_key = group_key
        self.api_version = api_version

    def getLongPoll(self, callback):
        #"{$server}?act=a_check&key={$key}&ts={$ts}&wait=25"
        
        r = requests.post(self.server, {'act': 'a_check', 'key': self.vk_key, 'ts': self.ts, 'wait': 25})
        response = r.json()
        logging.debug(response) # дебагаем
        if('error' in response):
            raise VkApiServerResponseError(response)
            #return

        self.new_ts = response['ts'] # события обработаны
        callback(response['updates'])

    def updateLongPoll(self):
        self.ts = self.new_ts

    def useMethod(self, method, params):
        api_url = "https://api.vk.com/method/" # url для обращения к API
        params.update({'access_token': self.group_key, 'v': self.api_version}) # additional keys
        logging.debug("useAPIMethod "+method) # дебагаем
        logging.debug(params) # дебагаем
        r = requests.post(api_url+method, params)
        response = r.json()
        logging.debug(response) # дебагаем
        if('error' in response):
            raise VkApiServerResponseError(response)
        print(response)
        return response

    def addKeyboard(self, name, path):
        with open(path, 'r', encoding="utf-8") as keyboard: # чтение файла с объектом клавиатуры
            self.keyboard[name] = keyboard.read()
    

class VkApiServerResponseError(Exception):
    def __init__(self, error_text):
        self.txt = error_text