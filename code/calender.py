from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

class Event:
    def __init__(self, name, date, time, city, state, isoCountry):
        self.name = name
        self.date = date
        self.time = time
        self.city = city
        self.state = state
        self.country = isoCountry

    def getName(self):
        return self.name
    
    def getDate(self):
        return self.date
    
    def getTime(self):
        return self.time

    def getCity(self):
        return self.city

    def getState(self):
        return self.state    

    def getCountry(self):
        return self.country

def getEvents():
    """
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events:\n')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        timeZone = "Australia/Melbourne",
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        #String containing the date
        startDateTime = event["start"]["dateTime"]

        #String containting event name
        eventName = event["summary"]

        #String containing location City State, Country
        location = event["location"]

        #seperating City & State string from Country
        locationSplit = location.split(', ', 1)
        cityAndState = locationSplit[0].rsplit(' ', 1) #rsplit for cities with spaces i.e. "Waurn Ponds")
        
        #isolating country from location
        country = locationSplit[1]
        
        #seperating city and state strings
        city = cityAndState[0]
        state = cityAndState[1]

        #String with date in YYYY-MM-DD format
        date = startDateTime[0:10:1] 

        #String with 24 hour time in HH:MM format with "Australia/Melbourne" as TimeZone
        time = startDateTime[11:16:1]

        event = Event(eventName, date, time, city, state, getISO3166(country))
        
        #Prints event details
        print("Event: " + event.getName() + "\n"
            + "Date: " + event.getDate() + " at " + event.getTime() + "\n"
            + "Location: " + event.getCity() + ", " + event.getState() +  ", " + event.getCountry() + "\n")

#TODO
#Add more country cases for getISO3166()

#Returns country in ISO3166 format
def getISO3166(country):
    if country == "Australia":
        isoCountry = "AU"

    elif country == "Japan":
        isoCountry = "JP"

    elif country == "New Zealand":
        isoCountry = "NZ"

    else:
        isoCountry = "ERROR"

    return isoCountry

def getEventName():
    return 

if __name__ == '__main__':
    getEvents()

