import sqlite3
#import json
import re
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from dateutil import parser
from matplotlib import style
style.use('fivethirtyeight')
connection = sqlite3.connect("sensor.db")
cursor = connection.cursor()

command = """
CREATE TABLE IF NOT EXISTS data (
entry INTEGER PRIMARY KEY,
time DATE,
temperature_C INTEGER,
humidity INTEGER);"""
cursor.execute(command)
print("How many times would you like this sensor to run?")
times = int(input())
for i in range(0, 3*times):
    s = str(input())
    s = s.replace("{", "")
    s = s.replace("}", "")
    data = s.split(",")
    format_str = """INSERT INTO data (entry, time, temperature_C, humidity)
    VALUES (NULL, "{time}", "{temp}", "{humidity}");"""
    for i, d in enumerate(data):
        if "time" in d:
            time = d.split(":")[1].strip()
        elif "temperature_C" in d:
            print("Temperature: " + d.split(":")[1].strip())
            temp = d.split(":")[1].strip()
        elif "humidity" in d:
            print("Humidity: " + d.split(":")[1].strip())
            humidity = d.split(":")[1].strip()
    command = format_str.format(time=time, temp=temp, humidity=humidity)
    cursor.execute(command)
    connection.commit()
cursor.execute('SELECT entry, temperature_C FROM data')
data2 = cursor.fetchall()

times = []
temps = []
    
for row in data2:
    times.append(row[0])
    temps.append(row[1])

plt.plot(times,temps,'-')
plt.show()
connection.close()
