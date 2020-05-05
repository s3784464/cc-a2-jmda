import requests

url = "https://api.weatherbit.io/v2.0/history/daily"

querystring = {"lang":"en","lon":"144.9631","lat":"37.8136"}

response = requests.request("GET", url, key = "b9dbf5b2f75940a0ab8a82f73caad54f", params=querystring)

print(response.text)