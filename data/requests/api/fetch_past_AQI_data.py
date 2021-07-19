# Sanitize the data by filling in missing dates and NaNs
# Air Now API

from itertools import cycle
import pandas as pd
import numpy as np
import requests
import time
import json

base_dir = "/home/jose/Programming/aiml/Data/houston-AQI-weather/data/"

with open("data/coords.json") as a: coords = json.load(a)
with open("data/API_keys.json") as b: keys = json.load(b)

different_keys = ['AN_API5', 'AN_API6']
key_pool = cycle(different_keys)

AN_API = keys[next(key_pool)]

def get_aqi(lat, long, date, key):
    return 'https://www.airnowapi.org/aq/observation/latLong/historical/?format=application/json&latitude={lat}&longitude={long}&date={date}T00-0000&distance=100&API_KEY={key}' \
        .format(lat=lat, long=long, date=date, key=key)

for name, coord in coords.items():
    lat, long = round(coord[0], 4), round(coord[1], 4)

    name = name.replace('/', '-')
    print(name)
    try:
        df = pd.read_csv("/home/jose/Programming/aiml/Data/houston-AQI-weather/filled-in-data/" + name + ".csv")
    except FileNotFoundError:
        df = pd.read_csv(base_dir + name + '.csv')
        del df['sky_ceiling_height']
    del df['Unnamed: 0']

    for i in range(len(df)):
        if (pd.isna(df.AQI.values[i]) or df.AQI.values[i] == 'NaN' or df.AQI.values[i] == 'NV') \
            and pd.to_datetime(df.Date.values[i], errors='coerce', format='%Y-%m-%d') >= np.datetime64('2012-01-01'):
            response_aqi = requests.get(get_aqi(lat, long, df.Date.values[i], keys[next(key_pool)]))
            
            try:
                print(response_aqi)
                df.AQI.values[i] = response_aqi.json()[0]['AQI']
            except (IndexError, KeyError):
                print('No data')
            except json.decoder.JSONDecodeError:
                print('Server error, skipping')
    
            print(df.loc[[i]])
            time.sleep(0.33)

        df.to_csv("/home/jose/Programming/aiml/Data/houston-AQI-weather/filled-in-data/" + name + ".csv")
    print(df.head(5))
    