from pushbullet import Pushbullet
import schedule
import time

key = "Your Own Key"

file1 = "files/monday.txt"
file2 = "files/tuesday.txt"
file3 = "files/wednesday.txt"
file4 = "files/thursday.txt"
file5 = "files/friday.txt"


def timetable1():
    with open(file1, "r") as f:
        text = f.read()
    send = Pushbullet(key)
    push = send.push_note("Reminder", text)
    return push

timetable1()


def timetable2():
    with open(file2, "r") as f:
        text = f.read()
    send = Pushbullet(key)
    push = send.push_note("Reminder", text)
    return push

timetable2()


def timetable3():
    with open(file3, "r") as f:
        text = f.read()
    send = Pushbullet(key)
    push = send.push_note("Reminder", text)
    return push

timetable3()


def timetable4():
    with open(file4, "r") as f:
        text = f.read()
    send = Pushbullet(key)
    push = send.push_note("Reminder", text)
    return push

timetable4()


def timetable5():
    with open(file5, "r") as f:
        text = f.read()
    send = Pushbullet(key)
    push = send.push_note("Reminder", text)
    return push

timetable5()

schedule.every().monday.at("06:00").do(timetable1)
schedule.every().tuesday.at("06:00").do(timetable2)
schedule.every().wednesday.at("06:00").do(timetable3)
schedule.every().thursday.at("06:00").do(timetable4)
schedule.every().friday.at("06:00").do(timetable5)


while True:
    schedule.run_pending()
    time.sleep(1)
