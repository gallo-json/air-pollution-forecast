import requests
import json

def get_weather(lat, long, date, key):
    return 'http://api.worldweatheronline.com/premium/v1/past-weather.ashx?key={key}&q={lat},{long}&format=json&date={date}&show_comments=no&tp=24' \
        .format(lat=lat, long=long, date=date, key=key)

with open("data/API_keys.json") as b: keys = json.load(b)

r = requests.get(get_weather(29, 95, '2015-01-01', keys['WWO_API1']))

print(r.status_code)