# KAYIEOT

Is minimalistic VK bot for students of KNRTU-KAI

  - use only one third party library (requests)
  - helps to check timetable
  - useless

### Features

  - Timetable for students
  - Timetable for lecturers
  - nothing else
  - 
  
## setup on your server
first install requirements
`ip install -r requirements.txt`

##### configure 
create file named config.json
`{
"VK_KEY": "your group key here",
"GROUP_ID": your group id here
}`

group key and group id you will find in group setting

also you must enable LongPoll API in group setting

setup finished. now run `python main.py`