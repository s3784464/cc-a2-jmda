import requests

url = "https://weatherbit-v1-mashape.p.rapidapi.com/current"

querystring = {"lang":"en","lon":"144.9631","lat":"37.8136"}

headers = {
    'x-rapidapi-host': "weatherbit-v1-mashape.p.rapidapi.com",
    'x-rapidapi-key': "200075a248mshbc2ad54f15e9399p19c4f8jsnb7c2e6391794"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)