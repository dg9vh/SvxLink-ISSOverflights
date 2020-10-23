import sqlite3
import time
import datetime
import requests
import json

conn = sqlite3.connect('iss_overflights.db')

c = conn.cursor()

url = 'http://api.open-notify.org/iss-pass.json?lat=49.2&lon=6.8&alt=210&n=10'
r = requests.get(url)
content = json.loads(r.content)
entries = (content["response"])
c.execute("DELETE FROM overflights WHERE 1")
# Save (commit) the changes
conn.commit()

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