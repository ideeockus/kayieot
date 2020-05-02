import vkapiserver
#import messageHandler
import storage
import handlers

import random

config = storage.getConfig() # ключ сообщества и id группы
vk_key = config['vk_key']
group_id = config['group_id']



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
            #mk = vkapiserv.keyboard['main'] # keyboard layout
            s_msg = s_msg_obj['s_msg']
            keyboard = s_msg_obj['keyboard']
            vkapiserv.useMethod("messages.send", {'user_id': user_id, 'random_id': random_id, 'message': s_msg, 'keyboard': keyboard})
    print("updtate")
    #storage.saveStorage()
    vkapiserv.updateLongPoll()
    vkapiserv.getLongPoll(gotEvents)


vkapiserv.getLongPoll(gotEvents)
