import requests
import json
from storage import make_s_msg_obj, users_storage, keyboards, state, timetable_output_mode
import logging

def handle(event):
    user_id = event['object']['message']['from_id']
    r_msg = event['object']['message']['text'] # received message
    #s_msg = "что-то пошло не так"
    #keyboard = keyboards['main']
    prepods_list = []
    try:
        prepods_list = getOptionsList(r_msg)
    except Exception as e:
        print("Ошибка при запросе расписания преподавателей")
        print(e)
    if(len(prepods_list)<1):
        s_msg = "Не могу найти преподавателя "+r_msg
        keyboard = keyboards['main']
        users_storage[user_id]['state'] = state.WAIT_PREPOD_NAME
        #s_msg_obj = make_s_msg_obj(s_msg, keyboard)
        #return s_msg_obj
    if(len(prepods_list)>1 and len(prepods_list)<=6):
        s_msg = "уточните, пожалуйста"
        keyboard = make_optionprepod_keyboard(prepods_list)
        users_storage[user_id]['state'] = state.WAIT_PREPOD_NAME
        #s_msg_obj = make_s_msg_obj(s_msg, keyboard)
        #return s_msg_obj
    if(len(prepods_list)>6):
        s_msg = "слишком много вариантов, уточните"
        keyboard = keyboards['main']
        users_storage[user_id]['state'] = state.WAIT_PREPOD_NAME
        #s_msg_obj = make_s_msg_obj(s_msg, keyboard)
        #return s_msg_obj
    if(len(prepods_list)==1):
        prepod_timetable = getPrepodTimetable(prepods_list[0])
        s_msg = f"Расписание преподавателя {prepods_list[0]['lecturer']}\n{formatPrepodTimetable(prepod_timetable)}"
        keyboard = keyboards['main']
        users_storage[user_id]['state'] = state.INACTION
        #s_msg_obj = make_s_msg_obj(s_msg, keyboard)
        #return s_msg_obj
    s_msg_obj = make_s_msg_obj(s_msg=s_msg, keyboard=keyboard)
    return s_msg_obj


def getOptionsList(text): # список возможных вариантов для text
    url1 = "https://kai.ru/for-staff/raspisanie?p_p_id=pubLecturerSchedule_WAR_publicLecturerSchedule10&p_p_lifecycle=2&p_p_resource_id=getLecturersURL&query=" #для prepod_login
    #s = requests.Session() # session
    r1 = requests.get(url1+text) # получение kai_id группы
    r1 = r1.json() # список возможных значений 
    return r1

def getPrepodTimetable(prepod):
    prepod_timetable_url = "https://kai.ru/raspisanie"
    url2 = "https://kai.ru/for-staff/raspisanie?p_p_id=pubLecturerSchedule_WAR_publicLecturerSchedule10&p_p_lifecycle=2&p_p_resource_id=schedule" # для расписания

    prepod_login = prepod['id']
    prepod_name = prepod['lecturer']
    r2 = requests.post(url2, {'prepodLogin': prepod_login})
    prepod_timetable = r2.json()
    return prepod_timetable

def formatPrepodTimetable(prepod_timetable):
    #weekdays = ["вс","пн","вт","ср","чт","пт","сб"]
    weekdays = ["вскресенье","понедельник","вторник","среда","четверг","пятница","суббота"]
    result = ""
    #result+="распиание для группы "+prepod+"\n"

    tabledays = prepod_timetable.keys() # список дней в расписании
    tabledays = sorted(tabledays) # сортировка дней в расписании
    for day in tabledays:
        #print(day)
        result = result + "📆" + weekdays[int(day)] + "\n"
        for lesson in prepod_timetable[day]:
            buildNum = lesson['buildNum'].strip().replace("-", "")
            buildSymbol = "🏟" if (buildNum.find("ОЛИМП")>-1) else  "🏛"
            #buildNum = buildNum + buildSymbol
            audNum = lesson['audNum'].strip().replace("-", "")
            build_aud = f"[{buildNum}{buildSymbol}, {audNum}]" # здание и аудитория
            if(buildNum==""): build_aud=f"[{audNum}]"
            if(audNum==""): build_aud=f"[{buildNum}{buildSymbol}]"
            if((buildNum=="") and (audNum=="")): build_aud=""
            if(buildNum!=""): buildNum = buildNum + buildSymbol
            dayTime = lesson['dayTime'].strip()
            disciplType = lesson['disciplType'].strip()
            disciplName = lesson['disciplName'].strip()
            group = lesson['group'].strip()
            dayDate = lesson['dayDate'].strip()
            if(dayDate=="ежн"): dayDate=""
            if(len(dayDate)>1): dayDate=f"({dayDate})"
            result = result+ f"{build_aud} {dayDate} {dayTime} - {disciplType}  у {group}\n"
            #logging.debug(result)
        result=result+"\n"
    return(result)

def make_optionprepod_keyboard(prepods_list):
    keyboard = {"inline": True, "buttons": []}
    """row = -1
    for i, prepod in enumerate(prepods_list): # The enumerate function gives us an iterable where each element is a tuple that contains the index of the item and the original item value
        if((i+1)==len(prepods_list)):
            keyboard['buttons'][row].append({'action': {'type': "text", 'label': prepod['lecturer']}})
            continue
        if(i%2==0):
            keyboard['buttons'].append([]) # обавление новой строки
            row+=1
        keyboard['buttons'][row].append({'action': {'type': "text", 'label': prepod['lecturer']}})"""
    for i, prepod in enumerate(prepods_list): # The enumerate function gives us an iterable where each element is a tuple that contains the index of the item and the original item value
        keyboard['buttons'].append([{'action': {'type': "text", 'label': prepod['lecturer']}}])
        #keyboard['buttons'][i]['action']['type'] = "text"
        #keyboard['buttons'][i][0]['action']['label'] = prepod['lecturer']
    keyboard = json.dumps(keyboard) # перевод словаря в json формат
    return keyboard