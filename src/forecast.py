import json
from pandas import DataFrame
import requests
from os import environ

environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  

from tensorflow.keras.models import load_model
from joblib import load
from numpy import expand_dims

from ml.model_utils import loss_mse_warmup

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
    r = requests.get(url(coords[region.replace('-', '/')])).json()

    arr = []
    # Unfortunately, the WeatherAPI free tier only allows a weather forecast of 3 days MAX
    # Cannot make this number higher unless I find another API that allows me to make a 5/7 weather forecast request reliably, or pay for a service
    # Could webscrape too
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

    # SEE: https://www2.dmu.dk/AtmosphericEnvironment/Expost/database/docs/PPM_conversion.pdf
    # https://www.airnow.gov/aqi/aqi-calculator/ 
    # ppb --> AQI line of best fit formula approximation
    # Air quality given in micrograms per cubic meter in json, so convert: ug/m^3 --> ppb --> AQI
    #arr[0][1] = 0.59 * (r["current"]["air_quality"]["o3"] / 2) + 6.1
    
    # Return dataframe of the dates to predict
    return DataFrame(arr, columns=['Date', 'AQI', 'air_temp', 'dew_point_temp', 'sea_level_pressure', 'visibility', 'wind_speed'])

weight_dir = 'weights/stations/'

def forecast_AQI(station_name):
    model = load_model(weight_dir + station_name + '/weights', custom_objects={'loss_mse_warmup': loss_mse_warmup})
    x_scaler = load(weight_dir + station_name + '/x-scaler.gz')
    y_scaler = load(weight_dir + station_name + '/y-scaler.gz')

    df = weather_forecast(station_name)
    x_data = df[['air_temp', 'dew_point_temp', 'sea_level_pressure', 'wind_speed', 'visibility']].values

    x = x_scaler.transform(x_data)
    x = expand_dims(x, axis=0)

    preds = model.predict(x)

    y_pred_rescaled = y_scaler.inverse_transform(preds[0]).ravel().astype(int)

    return y_pred_rescaled

# JSON to Pandas DF
arr = []
for region, coord in coords.items():
    arr.append([region, coord[0], coord[1]])

coords_df = DataFrame(arr, columns=['region', 'latitude', 'longitude'])