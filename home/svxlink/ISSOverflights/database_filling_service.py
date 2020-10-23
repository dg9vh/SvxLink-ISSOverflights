import sqlite3
import time
import datetime
import requests
import json
import configparser
import os

current_dir = os.getcwd()
# init configparser
config = configparser.ConfigParser()
config.read(current_dir + '/iss_overflights.ini')

conn = sqlite3.connect('iss_overflights.db')

c = conn.cursor()

# Cleaning overflight-table before filling with actual overflight-data because sometimes tracking-data changes
# and then two different lines for the same overflight are existing
c.execute("DELETE FROM overflights WHERE 1")
# Save (commit) the changes
conn.commit()

url = 'http://api.open-notify.org/iss-pass.json?lat='+config['DEFAULT']['lat']+'&lon='+config['DEFAULT']['lon']+'&alt='+config['DEFAULT']['alt']+'&n='+config['DEFAULT']['num']
print(url)
r = requests.get(url)
content = json.loads(r.content)
entries = (content["response"])

# Now for each entry calculate and write data into the database
for entry in entries:
    date_approach = time.strftime("%d.%m.%Y", time.localtime(entry['risetime']))
    time_approach = time.strftime("%H:%M", time.localtime(entry['risetime']))
    duration = int(entry['duration'])
    date_time_str = date_approach + ' ' + time_approach
    approach = datetime.datetime.strptime(date_time_str, '%d.%m.%Y %H:%M')
    los = approach + datetime.timedelta(seconds=duration)
    date_los = los.strftime("%d.%m.%Y")
    time_los = los.strftime("%H:%M")
    # Insert a row of data
    c.execute("INSERT OR REPLACE INTO overflights VALUES (?, ?, ?, ?, ?)",
              (date_approach, time_approach, duration, date_los, time_los))

    # Save (commit) the changes
    conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()