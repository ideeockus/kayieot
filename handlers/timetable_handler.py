import requests
import json
from storage import make_s_msg_obj, users_storage, keyboards, state
import logging

def handle(event):
    user_id = event['object']['message']['from_id']
    r_msg = event['object']['message']['text'] # received message
    #s_msg = "что-то пошло не так"
    #keyboard = keyboards['main']

    groups_list = getOptionsList(r_msg)
    if(len(groups_list)<1):
        s_msg = "Не могу найти группу "+r_msg
        keyboard = keyboards['main']
        users_storage[user_id]['state'] = state.INACTION
        #s_msg_obj = make_s_msg_obj(s_msg, keyboard)
        #return s_msg_obj
    if(len(groups_list)>1 and len(groups_list)<=10):
        s_msg = "уточните, пожалуйста"
        keyboard = make_optiongroup_keyboard(groups_list)
        users_storage[user_id]['state'] = state.WAIT_GROUP
        #s_msg_obj = make_s_msg_obj(s_msg, keyboard)
        #return s_msg_obj
    if(len(groups_list)>10):
        s_msg = "нужно уточнить группу"
        keyboard = keyboards['main']
        users_storage[user_id]['state'] = state.WAIT_GROUP
        #s_msg_obj = make_s_msg_obj(s_msg, keyboard)
        #return s_msg_obj
    if(len(groups_list)==1):
        timetable = getTimetable(groups_list[0])
        s_msg = f"Расписание для группы {groups_list[0]['group']}\n{formatTimetable(timetable)}"
        keyboard = keyboards['main']
        users_storage[user_id]['state'] = state.INACTION
        #s_msg_obj = make_s_msg_obj(s_msg, keyboard)
        #return s_msg_obj
    s_msg_obj = make_s_msg_obj(s_msg, keyboard)
    return s_msg_obj


def getOptionsList(text): # список возможных вариантов для text
    url1 = "https://kai.ru/raspisanie?p_p_id=pubStudentSchedule_WAR_publicStudentSchedule10&p_p_lifecycle=2&p_p_resource_id=getGroupsURL&query=" #для id группы
    #s = requests.Session() # session
    r1 = requests.get(url1+text) # получение kai_id группы
    r1 = r1.json() # список возможных значений 
    return r1

def getTimetable(group):
    timetable_url = "https://kai.ru/raspisanie"
    url2 = "https://kai.ru/raspisanie?p_p_id=pubStudentSchedule_WAR_publicStudentSchedule10&p_p_lifecycle=2&p_p_resource_id=schedule" # для расписания

    kai_group_id = group['id']
    kai_group_num = group['group']
    forma = group['forma']
    r2 = requests.post(url2, {'groupId': kai_group_id, 'programForm': forma})
    timetable = r2.json()
    return timetable

def formatTimetable(timetable):
    #weekdays = ["вс","пн","вт","ср","чт","пт","сб"]
    weekdays = ["вскресенье","понедельник","вторник","среда","четверг","пятница","суббота"]
    result = ""
    #result+="распиание для группы "+group+"\n"

    tabledays = timetable.keys() # список дней в расписании
    tabledays = sorted(tabledays) # сортировка дней в расписании
    for day in tabledays:
        #print(day)
        result = result + weekdays[int(day)] + "\n"
        for lesson in timetable[day]:
            buildNum = lesson['buildNum'].strip().replace("-", "")
            audNum = lesson['audNum'].strip().replace("-", "")
            build_aud = f"[{buildNum}, {audNum}]" # здание и аудитория
            if((buildNum=="") or (audNum=="")): build_aud=f"[{buildNum}{audNum}]"
            if((buildNum=="") and (audNum=="")): build_aud=""
            dayTime = lesson['dayTime'].strip()
            disciplType = lesson['disciplType'].strip()
            disciplName = lesson['disciplName'].strip()
            result = result+ f"{build_aud} {dayTime} {disciplType} - {disciplName}\n"
            logging.debug(result)
        result=result+"\n"
    return(result)

def make_optiongroup_keyboard(groups_list):
    keyboard = {"inline": True, "buttons": []}
    for i, group in enumerate(groups_list): # The enumerate function gives us an iterable where each element is a tuple that contains the index of the item and the original item value
        keyboard['buttons'].append([{'action': {'type': "text", 'label': "group_num"}}])
        #keyboard['buttons'][i]['action']['type'] = "text"
        keyboard['buttons'][i][0]['action']['label'] = group['group']
    keyboard = json.dumps(keyboard) # перевод словаря в json формат
    return keyboard