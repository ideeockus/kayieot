import vkapiserver
#import messageHandler
import storage
import handlers

import random

config = storage.getConfig() # ключ сообщества и id группы
vk_key = config['VK_KEY']
group_id = config['GROUP_ID']



vkapiserv = vkapiserver.vkApiServer(group_id, vk_key, 5.103)

storage.addKeyboard("main", "keyboards/main_keyboard.json") # загрузка клавиатуры
storage.addKeyboard("empty", "keyboards/empty_keyboard.json")
storage.addKeyboard("additional", "keyboards/additional_keyboard.json")

#storage.loadStorage()


def gotEvents(events):
    for event in events: # updtaes
        #print(event)
        if(event['type']=="message_new"):
            #s_msg_obj = messageHandler.handle(event)
            s_msg_obj = handlers.handle(event)
            user_id = event['object']['message']['from_id']
            random_id = random.randint(0, pow(2, 64)-1) # random id
            s_msg = s_msg_obj['s_msg']
            keyboard = s_msg_obj['keyboard']
            vkapiserv.useMethod("messages.send", {'user_id': user_id, 'random_id': random_id, 'message': s_msg, 'keyboard': keyboard})
    #storage.saveStorage()
    vkapiserv.updateLongPoll()
    #vkapiserv.getLongPoll(gotEvents) 

def start_bot():
    while(True):
        try:
            vkapiserv.getLongPoll(gotEvents) # "Внутри самого себя не найдешь бессмертия" - Антуан де Сент-Экзюпери
        except Exception as e:
            print("fatal error")
            print(e)
            vkapiserv.updateLongPoll()

start_bot()