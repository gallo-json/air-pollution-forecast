import json
from pandas import DataFrame
import requests

with open("data/coords.json") as a: coords = json.load(a)
with open("data/API_keys.json") as b: keys = json.load(b)

key = keys['WA_API']

def url(coordinates):
    return 'http://api.weatherapi.com/v1/forecast.json?key={key}&q={lat},{long}&days=10&aqi=yes&alerts=no' \
        .format(key=key, lat=coordinates[0], long=coordinates[1])

def weather_forecast(region):
    r = requests.get(url(coords[region])).json()
    arr = []
    for i in range(3):
        arr.append([r["forecast"]["forecastday"][i]["date"], 
                    None, 
                    r["forecast"]["forecastday"][i]["day"]["avgtemp_c"],
                    r["forecast"]["forecastday"][0]["day"]["avgtemp_c"] - (100 - r["forecast"]["forecastday"][i]["day"]["avghumidity"]) / 5,
                    r["current"]["pressure_mb"],
                    r["forecast"]["forecastday"][i]["day"]["avgvis_km"] * 1000,
                    r["forecast"]["forecastday"][i]["day"]["maxwind_mph"] / 3.2
                ])

    # Air quality given in micrograms / cubic meter --> ppb --> AQI
    arr[0][1] = 0.59 * (r["current"]["air_quality"]["o3"] / 2) + 6.1
    
    return DataFrame(arr, columns=['Date', 'AQI', 'air_temp', 'dew_point_temp', 'sea_level_pressure', 'visibility', 'wind_speed'])