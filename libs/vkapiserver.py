import requests
import json
import logging



logging.basicConfig(filename="vkApiServer.log", level=logging.DEBUG)
logging.info("loaded")
 

class vkApiServer:
    keyboard = {} # для хранения клавиатур
    def __init__(self, group_id, group_key, api_version=5.103):
        self.group_id = group_id
        self.group_key = group_key
        self.api_version = api_version

    def getLongPollServer(self):
        print("getting long poll server")
        logging.info("getting long poll server")
        api_url = "https://api.vk.com/method/" # url для обращения к API
        r = requests.post(api_url+"groups.getLongPollServer", {'group_id':self.group_id, 'access_token': self.group_key, 'v': self.api_version}) # данные сессии
        #if r.status_code != 200:
        response = r.json()
        logging.debug(response) # дебагаем
        if('error' in response):
            raise VkApiServerResponseError(response)
        self.vk_key = response['response']['key']
        self.server = response['response']['server']
        self.ts = response['response']['ts']

    def uploadDocForMessage(self, path, peer_id): # review this method
        api_url = "https://api.vk.com/method/"
        r = requests.post(api_url+"docs.getMessagesUploadServer", {'type': "doc", 'peer_id': peer_id, 'access_token': self.group_key, 'v': self.api_version})
        response = r.json()
        upload_url = response['response']['upload_url']

        files = {'file': open(path, 'rb')}
        r = requests.post(upload_url, files=files)
        uploading_file = r.json()['file']
        r = requests.post(api_url+"docs.save", {'file': uploading_file, 'access_token': self.group_key, 'v': self.api_version})

        r = r.json()
        file_type = r['response']['type']
        owner_id = str(r['response']['doc']['owner_id'])
        doc_id = str(r['response']['doc']['id'])
        attachment = file_type+ owner_id +"_"+doc_id
        return attachment


    def getLongPoll(self, callback): # запрос новых событий
        #"{$server}?act=a_check&key={$key}&ts={$ts}&wait=25"  
        r = requests.post(self.server, {'act': 'a_check', 'key': self.vk_key, 'ts': self.ts, 'wait': 25})
        response = r.json()
        logging.debug(response) # дебагаем
        if('error' in response): # ошибка в запросе
            raise VkApiServerResponseError(response)
        if('failed' in response): # ошибка у вк
            if(response['failed']==1): pass # история событий устарела или была частично утеряна, приложение может получать события далее, используя новое значение ts из ответа
            if(response['failed']==2 or response['failed']==3): # истекло время действия ключа или информация была утеряна
                self.getLongPollServer() # запрос long poll сервера
                r = requests.post(self.server, {'act': 'a_check', 'key': self.vk_key, 'ts': self.ts, 'wait': 25})
                response = r.json()

        self.new_ts = response['ts'] # события обработаны
        callback(response['updates'])


    def updateLongPoll(self): # обновление событий (чтобы вк не присылал уже обработанный)
        self.ts = self.new_ts


    def useMethod(self, method, params):
        api_url = "https://api.vk.com/method/" # url для обращения к API
        params.update({'access_token': self.group_key, 'v': self.api_version}) # additional keys
        logging.debug("useAPIMethod "+method) # дебагаем
        #logging.debug(params) # дебагаем
        r = requests.post(api_url+method, params)
        response = r.json()
        #logging.debug(response) # дебагаем
        if('error' in response):
            raise VkApiServerResponseError(response)
        #print(response)
        return response


    def addKeyboard(self, name, path):
        with open(path, 'r', encoding="utf-8") as keyboard: # чтение файла с объектом клавиатуры
            self.keyboard[name] = keyboard.read()
    

class VkApiServerResponseError(Exception): 
    def __init__(self, error_text):
        self.txt = error_text