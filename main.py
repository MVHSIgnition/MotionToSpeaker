#IMPORTANT: Need to run "pip install --upgrade google-api-python-client"
#           To get all the required modules

from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime
import time
from pprint import pprint
import requests 
import re
import os.path
import sys
numbers = re.compile('\d+(?:\.\d+)?')

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.
    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.
    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    """Shows basic usage of the Google Calendar API.
    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    now_utc = datetime.datetime.utcnow().isoformat() + 'Z'
    now = datetime.datetime.now().isoformat().split('.')[0]# + '+00:00' #+ 'Z' # 'Z' indicates UTC time
    endOfToday = now.replace(now.split('T')[1], '23:59:59')

    endOfToday_utc = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(time.mktime(time.strptime(endOfToday, "%Y-%m-%dT%H:%M:%S")))) + 'Z'
    
##    print(now_utc)
##    print(endOfToday_utc)
    print("Getting today's events...")
    eventsResult = service.events().list(
        calendarId='primary', timeMin=now_utc, timeMax=endOfToday_utc, singleEvents=True,
        orderBy='startTime').execute()
    #pprint(eventsResult)
    events = eventsResult.get('items', [])

    s = "Good morning. "
    if not events:
        print('No upcoming events found.')
        s += "You have no events scheduled today on your Google Calendar. "
    for i, event in enumerate(events):
        start = event['start'].get('dateTime', event['start'].get('date')).split('T')
        date = start[0]
        try:
            event_time = start[1].split('-')[0]
            print('time:', event_time)
        except:
            event_time = None
            #print(event)
##        time = int(start[1].split('-')[0].split(':')[0])
##        time -= time % 3
        
        print('title:', event['summary'])
        print('date:', date)
        
        try:
            zipcode = numbers.findall(event['location'])[-1] #find last number in the string (zipcode)
            city = event['location'].split(',')[1].strip()
            country = event['location'].split(',')[-1].strip() #find last
            print('location:', event['location'])
            print('zipcode:', zipcode)
            print('city:', city)
            print('country:', country)
        except:
            print('No Location Found.')
            zipcode = None
            city = None
            country = None

        try:
            r = requests.get('http://api.openweathermap.org/data/2.5/weather?q=' + city + ',' + country + '&mode=json&units=imperial&appid=93e7e9c55f90dbee5bb418ca0c517d19')
        except:
            try:
                r = requests.get('http://api.openweathermap.org/data/2.5/weather?zip=' + zipcode + ',' + country + '&mode=json&units=imperial&appid=93e7e9c55f90dbee5bb418ca0c517d19')
            except:
                print('Error loading weather data!')
                r = None
                temp_data = None
                weather_data = None
        
        if r:
            temp_data = r.json()['main'] #temperature data
            weather_data = r.json()['weather'][0] #weather data

            degree_sign = u'\N{DEGREE SIGN}'
            print('temp_max:', temp_data['temp_max'], degree_sign, 'F')
            print('temp_min:', temp_data['temp_min'], degree_sign, 'F')
            print('description:', weather_data['description'])
            print('\n')
        
        #pprint(r.json())
        if i == 0:
            s += "Today, according to your Google Calendar, %s is on your schedule" % (event['summary'])
        else:
            s += "%s is also on your schedule today" % (event['summary'])

        if event_time: 
            s += " at %s%s%s%s. " % (event_time.split(':')[0] if int(event_time.split(':')[0]) < 13 else str(int(event_time.split(':')[0]) - 12), ':' + event_time.split(':')[1] if event_time.split(':')[1] != '00' else ' o\'clock', ' am' if int(event_time.split(':')[0]) < 13 else ' pm', ' in ' + city if city else "")
        else:
            s += ". "

        if r:
            s += "The weather conditions there will be %s, with a maximum temperature of %s degrees Fahrenheit and a minimum temperature of %s degrees Fahrenheit. " % (weather_data['description'], temp_data['temp_max'], temp_data['temp_min'])
        else:
            s += "Weather could not be found for this event. "
    
    s += "Have a nice day!"
    print(s)
    os.system('pico2wave -w say.wav "' + s + '" && aplay say.wav')
        
if __name__ == '__main__':
    while(1):
        if(os.path.isfile("/home/pi/dev/rtl_433/gfile001.data")):
            os.system('rm /home/pi/dev/rtl_433/gfile001.data')
            main()
            break
