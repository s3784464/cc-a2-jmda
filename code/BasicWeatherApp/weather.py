from datetime import datetime
import os
import pytz
import requests
import math
API_KEY = '9b18e2941607b2d54150439c9ad80bfe'
API_URL = ('https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=minutely,hourly&appid={}')
#API_URL = ('http://api.openweathermap.org/data/2.5/weather?q=Melbourne&mode=json&units=metric&appid=9b18e2941607b2d54150439c9ad80bfe')
#API_URL = ('https://api.openweathermap.org/data/2.5/onecall?lat=33.441792&lon=-94.037689&exclude=minutely,hourly&appid=9b18e2941607b2d54150439c9ad80bfe')
#API_URL = ('https://api.openweathermap.org/data/2.5/onecall?{}&exclude=minutely,hourly&appid={}')

GEO_KEY = 'JFeFmdyX5dFybKA3rMVnxzPEk9vZ8_ZzKavdsJHcSbs'
GEO_URL = ('https://geocode.search.hereapi.com/v1/geocode?apikey={}&q={}')

def query_api(event):
    try:
        loc = event.getCity()
        coord = requests.get(GEO_URL.format(GEO_KEY, loc)).json()
        lat = coord['items'][0]['position']['lat']
        lon = coord['items'][0]['position']['lng']
        data = requests.get(API_URL.format(lat, lon, API_KEY)).json()
    except Exception as exc:
        print(exc)
        data = None
    return data 


def improve_weather_prediction(actual):
    requests.get('https://us-central1-cc-s3784464-a2.cloudfunctions.net/ImproveWeatherForecast')
    average = 20
    predicted = ((average + actual) / 2) * 0.01 + 0.99 * actual
    average = (average + predicted) / 2
    return predicted