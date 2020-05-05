#url = "https://api.weatherbit.io/v2.0/history/daily"
#response = requests.request("GET", url, key = "b9dbf5b2f75940a0ab8a82f73caad54f", params=querystring)

from weatherbit.api import Api
api_key = "b9dbf5b2f75940a0ab8a82f73caad54f"
api = Api(api_key)

# Set the granularity of the API - Options: ['daily','hourly','3hourly']
# Will only affect forecast requests.
api.set_granularity('daily')

forecast = api.get_forecast(city="Geelong", state="Victoria", country="AU", units='M')
print(forecast.get_series(['temp','precip']))
#print(api.get_history(city="Geelong", state="Victoria", country="AU", units='M', start_date="2020-04-04", end_date="2020-04-05"))


# # You can also query by city:
# forecast = api.get_forecast(city="Raleigh,NC")

# # Or City, state, and country:
# forecast = api.get_forecast(city="Raleigh", state="North Carolina", country="US")


# # To get a daily time series of temperature, precipitation, and rh:
# print forecast.get_series(['precip','temp','rh'])

# # Get hourly history by lat/lon
# api.set_granularity('hourly')
# history = api.get_history(lat=lat, lon=lon, start_date='2018-02-01',end_date='2018-02-02')


# ...
