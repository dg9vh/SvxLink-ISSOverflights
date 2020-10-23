import sqlite3
import time
import datetime
import os
from os import path

# datetime object containing current date and time
now = datetime.datetime.now().replace(second=0, microsecond=0)

conn = sqlite3.connect('iss_overflights.db')

message_filepath = "ISS.txt"

if path.exists(message_filepath):
    os.remove(message_filepath)

c = conn.cursor()

for row in c.execute('SELECT * FROM overflights ORDER BY date, time'):
    date_approach = row[0]
    time_approach = row[1]
    date_los = row[3]
    time_los = row[4]

    date_time_str = date_approach + ' ' + time_approach
    approach = datetime.datetime.strptime(date_time_str, '%d.%m.%Y %H:%M')


    los_str = date_los + ' ' + time_los
    los = datetime.datetime.strptime(los_str, '%d.%m.%Y %H:%M')

    duration = time.strftime(" %M Minuten und %S Sekunden", time.gmtime(row[2]))

    if (duration[16] == "0"):
        duration = duration[0:16] + duration[17:]

    if (duration[1] == "0"):
        duration = " " + duration[2:]
    duration = duration.replace(" 1 Minuten ", " einer Minute ")
    duration = duration.replace(" 1 Sekunden", " einer Sekunde")

    if now == approach - datetime.timedelta(minutes=15):
        message_file = open(message_filepath, 'w')
        message_file.write("ISS Überflug in fünfzehn Minuten, Dauer:" + duration)
        message_file.close()

    if now == approach - datetime.timedelta(minutes=1):
        message_file = open(message_filepath, 'w')
        message_file.write("ISS Überflug in einer Minute, Dauer:" + duration)
        message_file.close()

    if now == los:
        message_file = open(message_filepath, 'w')
        message_file.write("ISS Überflug beendet, Radiohorizont verlassen.")
        message_file.close()
