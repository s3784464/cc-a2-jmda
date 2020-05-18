from datetime import datetime
import os
import pytz
import requests
import math
API_KEY = '9b18e2941607b2d54150439c9ad80bfe'
#API_URL = ('http://api.openweathermap.org/data/2.5/weather?q=Melbourne&mode=json&units=metric&appid=9b18e2941607b2d54150439c9ad80bfe')
API_URL = ('https://api.openweathermap.org/data/2.5/onecall?lat=33.441792&lon=-94.037689&exclude=minutely,hourly&appid=9b18e2941607b2d54150439c9ad80bfe')

def query_api(city):
    try:
        #print(API_URL.format(city, API_KEY))
        #data = requests.get(API_URL.format(city, API_KEY)).json()
        data = requests.get(API_URL).json()
    except Exception as exc:
        print(exc)
        data = None
    return data 