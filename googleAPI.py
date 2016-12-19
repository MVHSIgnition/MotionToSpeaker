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

from pprint import pprint
import requests 

import re
numbers = re.compile('\d+(?:\.\d+)?')
def main():
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    eventsResult = service.events().list(
        calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
        orderBy='startTime').execute()
    pprint(eventsResult)
    events = eventsResult.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date')).split('T')
        date = start[0]
        time = int(start[1].split('-')[0].split(':')[0])
        time -= time % 3
        zipcode = numbers.findall(event['location'])[-1] #find last number in the string (zipcode)
        city = event['location'].split(',')[1].strip()
        country = event['location'].split(',')[-1].strip() #find last
        
        print('title:', event['summary'])
        print('date:', date)
        print('time:', time)
        print('location:', event['location'])
        print('zipcode:', zipcode)
        print('city:', city)
        print('country:', country)
        print('\n')

        try:
            r = requests.get('http://api.openweathermap.org/data/2.5/weather?q=' + city + ',' + country + '&mode=json&units=imperial&appid=93e7e9c55f90dbee5bb418ca0c517d19')
        except:
            try:
                r = requests.get('http://api.openweathermap.org/data/2.5/weather?zip=' + zipcode + ',' + country + '&mode=json&units=imperial&appid=93e7e9c55f90dbee5bb418ca0c517d19')
            except:
                print('Error loading weather data!')
                continue

        #below is if url is "data/2.5/forecast?" (forecasted data, can get for specific times in the future)
##        weather_data = r.json().get('list')
##        for d in weather_data:
##            if str(time) in d['dt_txt']: #fix because only does the most recent date
##                print(d['dt_txt'])
##                print('temp_max:', d['main']['temp_max'])
##                print('temp_min:', d['main']['temp_min'])
##                break

        #below is if url is "data/2.5/weather?" (current data)
        temp_data = r.json()['main'] #temperature data
        weather_data = r.json()['weather'][0] #weather data

        degree_sign = u'\N{DEGREE SIGN}'
        print('temp_max:', temp_data['temp_max'], degree_sign, 'F')
        print('temp_min:', temp_data['temp_min'], degree_sign, 'F')
        print('description:', weather_data['description'])
        
        
        #pprint(r.json())

##        os.system("say -v " + event['summary'])

if __name__ == '__main__':
    main()
