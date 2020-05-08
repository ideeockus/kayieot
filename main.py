from libs import vkapiserver
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


def gotEvents(events):
    for event in events: # updtaes
        if(event['type']=="message_new"):
            s_msg_obj = handlers.handle(event)
            #r_msg_len = len(event['object']['message']['text'])
            #if(r_msg_len>200): s_msg_obj = {'message': "кажется сообщение слишком длинное", 'keyboard': storage.keyboards['main']}
            user_id = event['object']['message']['from_id']
            random_id = random.randint(0, pow(2, 64)-1) # random id # nosec
            s_msg_params = {'user_id': user_id, 'random_id': random_id}
            for key, value in s_msg_obj.items():
                s_msg_params[key] = value
            vkapiserv.useMethod("messages.send",  s_msg_params)
    vkapiserv.updateLongPoll()


def start_bot():
    vkapiserv.getLongPollServer()
    while(True):
        vkapiserv.getLongPoll(gotEvents)

start_bot()