# Sanitize the data by filling in missing dates and NaNs

# Fetch historical weather only data
# https://www.worldweatheronline.com

# Air Now 

from datetime import datetime
import pandas as pd 
import requests
import time
import json

base_dir = "/home/jose/Programming/aiml/Data/houston-AQI-weather/data/"

with open("data/coords.json") as a: coords = json.load(a)
with open("data/API_keys.json") as b: keys = json.load(b)

AN_API = keys['AN_API']

def get_aqi(lat, long, date):
    return 'https://www.airnowapi.org/aq/observation/latLong/historical/?format=application/json&latitude={lat}&longitude={long}&date={date}T00-0000&distance=100&API_KEY={key}' \
        .format(lat=lat, long=long, date=date, key=AN_API)


'''
response_aqi = requests.get(get_aqi(29.1442, -95.7566, '2019-02-02'))

print(response_aqi.json()[0]['AQI'])

response_weather = requests.get(get_weather(29.1442, -95.7566, '2019-02-02'))

# air_temp
print(response_weather.json()['data']['weather'][0]['maxtempC'])

# dew point temp
print(response_weather.json()['data']['weather'][0]['hourly'][0]['DewPointC'])

# sea level pressure
print(response_weather.json()['data']['weather'][0]['hourly'][0]['pressure'])

# visibility
print(response_weather.json()['data']['weather'][0]['hourly'][0]['visibility']) # multiply by 1000

#wind speed
print(response_weather.json()['data']['weather'][0]['hourly'][0]['windspeedKmph']) # DIVIDE BY 3.6 FOR m/s
'''

for name, coord in coords.items():
    lat, long = round(coord[0], 4), round(coord[1], 4)

    name = name.replace('/', '-')
    try:
        df = pd.read_csv("/home/jose/Programming/aiml/Data/houston-AQI-weather/filled-in-data/" + name + ".csv")
    except FileNotFoundError:
        df = pd.read_csv(base_dir + name + '.csv')
        del df['sky_ceiling_height']
    del df['Unnamed: 0']

    print(name)
    for i in range(len(df)):
        try:
            if (pd.isna(df.AQI.values[i]) or df.AQI.values[i] == 'NaN' or df.AQI.values[i] == 'NV') and (datetime.strptime(df.Date.values[i], '%Y-%m-%d') >= datetime(2012, 1, 1)):
                response_aqi = requests.get(get_aqi(lat, long, df.Date.values[i]))
                
                try:
                    print(response_aqi)
                    df.AQI.values[i] = response_aqi.json()[0]['AQI']
                except (IndexError, KeyError):
                    print('No data')
                except json.decoder.JSONDecodeError:
                    print('Server error, skipping')
        
                print(df.loc[[i]])
                time.sleep(1)
        except TypeError:
            print('Skipping...')

        df.to_csv("/home/jose/Programming/aiml/Data/houston-AQI-weather/filled-in-data/" + name + ".csv")
    print(df.head(5))
    