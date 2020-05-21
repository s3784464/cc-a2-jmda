# Google Calender API
from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Google Cloud Datastore
from google.cloud import datastore

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


class Event:
    def __init__(self, name, date, time, city, state, country):
        self.name = name
        self.date = date
        self.time = time
        self.city = city
        self.state = state
        self.country = country

    def getName(self):
        return self.name

    def getDate(self):
        return self.date

    def getDay(self):
        today = datetime.date.today()
        #future = datetime.datetime.strptime(self.date, "%Y-%m-%d").date()
        future = datetime.date.today() + datetime.timedelta(days=1)
        delta =  (today - future).days
        return delta

    def getTime(self):
        return self.time

    def getCity(self):
        return self.city

    def getState(self):
        return self.state

    def getCountry(self):
        return self.country

    # prints event details
    def print(self):
        print("Event: " + self.name + "\n"
              + "Date: " + self.date + " at " + self.time + "\n"
              + "Location: " + self.city + ", " + self.state + ", " + self.country + "\n")


class Calender:
    client = datastore.Client.from_service_account_json(
        'cc-s3784464-a2-4896da251496.json')

    def buildEvents(self):
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
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print('Getting the upcoming 7 events:\n')
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=7, singleEvents=True,
                                              timeZone="Australia/Melbourne",
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')

        eventNo = 0
        entityName = "event"
        arr = []
        for event in events:
            eventNo = eventNo + 1
            # String containing the date
            startDateTime = event["start"]["dateTime"]

            # String containing event name
            eventName = event["summary"]

            # String containing location City State, Country
            location = event["location"]

            # seperating City & State string from Country
            locationSplit = location.split(', ', 1)
            # rsplit for cities with spaces i.e. "Waurn Ponds")
            cityAndState = locationSplit[0].rsplit(' ', 1)

            # isolating country from location
            country = locationSplit[1]

            # seperating city and state strings
            city = cityAndState[0]
            state = cityAndState[1]

            # String with date in YYYY-MM-DD format
            date = startDateTime[0:10:1]

            # String with 24 hour time in HH:MM format with "Australia/Melbourne" as TimeZone
            time = startDateTime[11:16:1]

            # create new event object
            event = Event(eventName, date, time, city,
                          state, self.getISO3166(country))

            arr.append(event)

            # create datastore entity
            name = entityName + str(eventNo)
            event_key = self.client.key('event', name)
            dsEvent = datastore.Entity(key=event_key)
            self.addToDatastore(dsEvent, event)

            event.print()
        return arr

    def addToDatastore(self, dsEvent, eventObject):
        dsEvent['name'] = eventObject.getName()
        dsEvent['date'] = eventObject.getDate()
        dsEvent['time'] = eventObject.getTime()
        dsEvent['city'] = eventObject.getCity()
        dsEvent['state'] = eventObject.getState()
        dsEvent['country'] = eventObject.getCountry()

        #add the event entity to the datastore
        self.client.put(dsEvent)

    # Returns country in ISO3166 format
    def getISO3166(self, country):
        if country == "Australia":
            isoCountry = "AU"

        elif country == "Japan":
            isoCountry = "JP"

        elif country == "New Zealand":
            isoCountry = "NZ"

        else:
            isoCountry = "ERROR"

        # TODO
        # Add more country cases for getISO3166()
        return isoCountry
