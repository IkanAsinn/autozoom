import requests
import webbrowser
from csv import writer, reader
from json import loads
from pandas import read_csv
from getpass import getpass
from os import system, remove
from time import strftime, sleep
from datetime import timedelta

def printLogo():
    print('''
   _____          __        __________                     
  /  _  \  __ ___/  |_  ____\____    /____   ____   _____  
 /  /_\  \|  |  \   __\/  _ \ /     //  _ \ /  _ \ /     \ 
/    |    \  |  /|  | (  <_> )     /(  <_> |  <_> )  Y Y  \\
\____|__  /____/ |__|  \____/_______ \____/ \____/|__|_|  /
        \/                          \/                  \/
''')

def autoZoom():
    system('cls')
    printLogo()
    try:
        file = open('schedule.csv', 'r')
        readed = reader(file, delimiter=',')
        schedule = []
        for row in readed:
            if len(row) > 0:
                schedule.append(row)

        file.close()

    except FileNotFoundError:
        print('Please use get schedule first!')
        input('Press enter to continue...')
        return

    today = strftime("%d/%m/%Y")
    today = changeFormat(today)

    isStarted = False
    try:
        for i in range(1, len(schedule)):
            print("Next Schedule:", schedule[i][0], "at", schedule[i][1])
            print("Class Name: {} - {}".format(schedule[i][4], schedule[i][5]))
            print('Press Ctrl-C to close')
            while True:
                if isStarted == False:
                    hour = int(strftime("%H"))
                    minute = int(strftime("%M"))
                    start_hour = int(schedule[i][1].split(':')[0])
                    start_minute = int(schedule[i][1].split(':')[1])
                    start_date = schedule[i][0]
                    sleep(1)
                    if hour >= start_hour and minute >= start_minute - 10 and today == start_date: # 10 minutes before class
                        isStarted = True

                    if hour >= 24:
                        today = changeFormat(strftime("%d/%m/%Y"))

                if isStarted == True:
                    webbrowser.open(schedule[i][8])
                    end_hour = int(schedule[i][2].split(':')[0])
                    end_minute = int(schedule[i][2].split(':')[1])
                    start_hour = int(schedule[i][1].split(':')[0])
                    start_minute = int(schedule[i][1].split(':')[1])
                    end_hour *= 3600
                    end_minute *= 60
                    start_hour *= 3600
                    start_minute *= 60
                    duration = ((end_hour + end_minute) - (start_hour + start_minute) - 300)
                    print('Class Started')
                    class_code = schedule[i][4]
                    class_name = schedule[i][5]
                    lines = list()
                    with open('schedule.csv', 'r') as f:
                        readed_file = reader(f)
                        for row in readed_file:
                            lines.append(row)

                    with open('schedule.csv', 'w') as f:
                        output = writer(f)
                        for row in lines:
                            if len(row) > 0:
                                if row[0] != schedule[i][0] and row[1] != schedule[i][1]:
                                    output.writerow(row)

                    while duration > 0:
                        print('Class: {} - {}'.format(class_code, class_name))
                        print('Time Left:', timedelta(seconds=duration))
                        sleep(1)
                        duration -= 1
                        system('cls')
                    isStarted = False
                    break
        
    except KeyboardInterrupt:
        print('[q]uit | [c]ontinue')
        choice = input()
        if choice == 'q':
            return
        elif choice == 'c':
            autoZoom()

def getSchedule():
    print('Getting schedule data...\n')
    r = s.get(url + '/Home/GetViconSchedule')

    with open('schedule.json', 'w') as f:
        f.write(r.text)

    schedule_data = open('schedule.json', 'r').read()
    x = loads(schedule_data)
    fullName = x[0]['FullName']

    remove('schedule.json')

    file = open('schedule.csv', 'w')

    f = writer(file)

    f.writerow(["DisplayStartDate", "StartTime", "EndTime", "ClassCode", "CourseCode", "CourseTitleEn", "MeetingId", "MeetingPassword", "MeetingUrl"])

    for x in x:
        f.writerow([x['DisplayStartDate'], x['StartTime'], x['EndTime'], x['ClassCode'], x['CourseCode'], x['CourseTitleEn'], x['MeetingId'], x['MeetingPassword'], x['MeetingUrl']])

    file.close()

    schedule = open('schedule.csv', 'r')
    readed = read_csv(schedule)

    print('Hello ' + fullName + '!')
    print('Your schedule is:' + '\n')
    print(readed)

    schedule.close()

    print('\nYour schedule is saved to schedule.csv')
    print('Have a nice day!')
    input('Press enter to continue...')

def changeFormat(date: str):
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    day, month, year = date.split('/')
    month = months[int(month) - 1]
    return f'{day} {month} {year}'


if __name__ == '__main__':
    s = requests.Session()
    url = 'https://myclass.apps.binus.ac.id/'
    status = False

    while not status:
        printLogo()
        print('BinusMaya Login')
        print('===============')
        username = input("Username: ")
        password = getpass()
        if '@' in username:
            username = username.split('@')[0]

        data = {
            'Username': username,
            'Password': password
        }
        r = s.post(url + '/Auth/Login', data=data)
        resp_status = r.json()
        status = resp_status.get('Status')
        if status == True:
            print('Login Success\n')
            break
        else:
            print('Login Failed')
            input('Press enter to try again')
            system('cls')


    while True:
        system('cls')
        printLogo()
        print('1. Get Schedule')
        print('2. Start Autozoom')
        print('3. Exit')
        choice = int(input('>> '))
        
        if choice == 1:
            getSchedule()
        
        elif choice == 2:
            autoZoom()

        elif choice == 3:
            break

    print('\nGoodbye!!')