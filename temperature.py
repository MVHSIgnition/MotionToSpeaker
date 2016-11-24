#contains code for collecting data from temperature sensor

import sqlite3
#import json
import re
connection = sqlite3.connect("sensor.db")
cursor = connection.cursor()
#only execute the below if sensor.db does not exist
##command = """
##CREATE TABLE data (
##entry INTEGER PRIMARY KEY,
##time DATE,
##temperature_C INTEGER,
##humidity INTEGER);"""
##cursor.execute(command)
##cursor.execute("SELECT * FROM data")
##for i in cursor.fetchall():
##    print(i)
while True:
    s = str(input())
    s = s.replace("{", "")
    s = s.replace("}", "")
    s = s.replace("\"", "")
    data = s.split(",")
    format_str = """INSERT INTO data (entry, time, temperature_C, humidity)
    VALUES (NULL, "{time}", "{temp}", "{humidity}");"""
    for i, d in enumerate(data):
        if "time" in d:
            time = d.split(":", 1)[1].strip()
        elif "temperature_C" in d:
            print("Temperature: " + d.split(":")[1].strip())
            temp = d.split(":", 1)[1].strip()
        elif "humidity" in d:
            print("Humidity: " + d.split(":")[1].strip())
            humidity = d.split(":", 1)[1].strip()
    command = format_str.format(time=time, temp=temp, humidity=humidity)
    cursor.execute(command)
    connection.commit()
connection.close()


