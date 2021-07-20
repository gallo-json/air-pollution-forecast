# Fetch historical weather data
# https://www.worldweatheronline.com API free 60-day trial
# Similar logic to fetch_past_AQI_data.py

from itertools import cycle
import numpy as np
import pandas as pd 
import requests
import time
import json

base_dir = "/home/jose/Programming/aiml/Data/houston-AQI-weather/data/" # Directories where all the CSV files are located
new_dir = "/home/jose/Programming/aiml/Data/houston-AQI-weather/filled-in-data/"

with open("data/coords.json") as a: coords = json.load(a) # Load region names and respective coordinates
with open("data/API_keys.json") as b: keys = json.load(b) # JSON file where all API keys are located

# Create array of all API keys in order to cycle over them
different_keys = ['WWO_API2', 'WWO_API3', 'WWO_API4', 'WWO_API5', 'WWO_API6']
key_pool = cycle(different_keys)

# Helper function to return URL ready to request
def get_weather(lat, long, date, key):
    return 'http://api.worldweatheronline.com/premium/v1/past-weather.ashx?key={key}&q={lat},{long}&format=json&date={date}&show_comments=no&tp=24' \
        .format(lat=lat, long=long, date=date, key=key)

for name, coord in coords.items(): # Loop over all regions
    lat, long = round(coord[0], 4), round(coord[1], 4) # Get coordinates and round them

    name = name.replace('/', '-')
    print(name)

    # Making copies of the CSV files in base_dir into new_dir but filled up with weather data
    try:
        df = pd.read_csv(new_dir + name + ".csv")
    except FileNotFoundError:
        df = pd.read_csv(base_dir + name + '.csv')
        del df['sky_ceiling_height'] # The API does not have this class so delete it
    del df['Unnamed: 0'] # Delete default column
    
    for i in range(len(df)):
        # We are tring to fill in missing values, so check if NaN, 'NA', or 'NV' exists   
        # Unfortunately, the historical API only goes back to 2012
        if any((pd.isna(df[label].values[i]) or df[label].values[i] == 'NaN' or df[label].values[i] == 'NV') for label in list(df.columns[2:])) \
            and pd.to_datetime(df.Date.values[i], errors='coerce', format='%Y-%m-%d') >= np.datetime64('2012-01-01'):

            # Make a request to the URL cycling the API keys
            response_weather = requests.get(get_weather(lat, long, df.Date.values[i], key=keys[next(key_pool)]))

            print(response_weather)
            try:
                # Fill in all the respective weather classes
                if (pd.isna(df.air_temp.values[i]) or df.air_temp.values[i] == 'NaN' or df.air_temp.values[i] == 'NV'):
                    df.air_temp.values[i] = int(response_weather.json()['data']['weather'][0]['maxtempC'])
                
                if (pd.isna(df.dew_point_temp.values[i]) or df.dew_point_temp.values[i] == 'NaN' or df.dew_point_temp.values[i] == 'NV'):
                    df.dew_point_temp.values[i] = int(response_weather.json()['data']['weather'][0]['hourly'][0]['DewPointC'])

                if (pd.isna(df.sea_level_pressure.values[i]) or df.sea_level_pressure.values[i] == 'NaN' or df.sea_level_pressure.values[i] == 'NV'):
                    df.sea_level_pressure.values[i] = int(response_weather.json()['data']['weather'][0]['hourly'][0]['pressure'])

                if (pd.isna(df.visibility.values[i]) or df.visibility.values[i] == 'NaN' or df.visibility.values[i] == 'NV'):
                    # Convert km to m
                    df.visibility.values[i] = float(response_weather.json()['data']['weather'][0]['hourly'][0]['visibility']) * 1000

                if (pd.isna(df.wind_speed.values[i]) or df.wind_speed.values[i] == 'NaN' or df.wind_speed.values[i] == 'NV'):
                    # Convert kph to m/s
                    df.wind_speed.values[i] = float(response_weather.json()['data']['weather'][0]['hourly'][0]['windspeedKmph']) / 3.2
            # Sometimes the API will mess up and return bad JSON, so temporary solution for now
            except (KeyError, json.decoder.JSONDecodeError):
                print('Bad data, skipping...')

            print(df.loc[[i]])
            
            # We dont want to request the API without time breaks
            time.sleep(0.33)
        # Write to the new csv file in new_dir
        df.to_csv(new_dir + name + ".csv")
    print(df.head(5))