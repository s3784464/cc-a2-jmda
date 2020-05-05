#url = "https://api.weatherbit.io/v2.0/history/daily"
#response = requests.request("GET", url, key = "b9dbf5b2f75940a0ab8a82f73caad54f", params=querystring)

from weatherbit.api import Api
api_key = "b9dbf5b2f75940a0ab8a82f73caad54f"
api = Api(api_key)

# Set the granularity of the API - Options: ['daily','hourly','3hourly']
# Will only affect forecast requests.
api.set_granularity('hourly')

forecast = api.get_forecast(city="Geelong", state="Victoria", country="AU", units='M')
#print(forecast.get_series('temp'))
print(forecast.get_history())


# # You can also query by city:
# forecast = api.get_forecast(city="Raleigh,NC")

# # Or City, state, and country:
# forecast = api.get_forecast(city="Raleigh", state="North Carolina", country="US")

# # To get a daily forecast of temperature, and precipitation:
# print forecast.get_series(['temp','precipitation'])


# # To get a daily time series of temperature, precipitation, and rh:
# print forecast.get_series(['precip','temp','rh'])

# # Get hourly history by lat/lon
# api.set_granularity('hourly')
# history = api.get_history(lat=lat, lon=lon, start_date='2018-02-01',end_date='2018-02-02')

# # To get an hourly time series of temperature, precipitation, and rh:
# print forecast.get_series(['precip','temp','rh'])

# ...
# ```

# The ``get_forecast()`` method requires named parameters. The current choices are either (lat=..., lon=...), (city="City,ST"), or (city=..., state=..., country=...)
