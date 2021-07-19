import json
from pandas import DataFrame
import requests

# Load in each region's coordinates
with open("data/coords.json") as a: coords = json.load(a)
with open("data/API_keys.json") as b: keys = json.load(b)

# API key
key = keys['WA_API']

# Helper function that returns the url ready to use
def url(coordinates):
    return 'http://api.weatherapi.com/v1/forecast.json?key={key}&q={lat},{long}&days=10&aqi=yes&alerts=no' \
        .format(key=key, lat=coordinates[0], long=coordinates[1])

def weather_forecast(region):
    # Make API request from link
    r = requests.get(url(coords[region])).json()

    arr = []
    # Unfortunately, the WeatherAPI free tier only allows a weather forecast of 3 days MAX
    # Cannot make this number higher unless I find another API that allows me to make a 5/7 weather forecast request reliably, or pay for a service
    # Could webscrape
    for i in range(3):
        arr.append([r["forecast"]["forecastday"][i]["date"], 
                    None, # This is what we're trying to predict, so it's left blank
                    r["forecast"]["forecastday"][i]["day"]["avgtemp_c"],
                    # SEE: https://en.wikipedia.org/wiki/Dew_point#Simple_approximation
                    # Dew point simple approximation formula given humidity and current temperature 
                    # Only works when humidity is over 50, but Houston's humididty will always be over 50
                    r["forecast"]["forecastday"][0]["day"]["avgtemp_c"] - (100 - r["forecast"]["forecastday"][i]["day"]["avghumidity"]) / 5,
                    r["current"]["pressure_mb"],
                    r["forecast"]["forecastday"][i]["day"]["avgvis_km"] * 1000, # Convert from km to m
                    r["forecast"]["forecastday"][i]["day"]["maxwind_kph"] / 3.2 # Convert from kph to m/s
                ])

    # https://www2.dmu.dk/AtmosphericEnvironment/Expost/database/docs/PPM_conversion.pdf
    # Air quality given in micrograms per cubic meter in json
    # Convert: --> ppb --> AQI
    arr[0][1] = 0.59 * (r["current"]["air_quality"]["o3"] / 2) + 6.1
    
    # Return dataframe of the dates to predict
    return DataFrame(arr, columns=['Date', 'AQI', 'air_temp', 'dew_point_temp', 'sea_level_pressure', 'visibility', 'wind_speed'])