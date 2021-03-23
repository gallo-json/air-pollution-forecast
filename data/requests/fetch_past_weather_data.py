
import pandas as pd 
import requests
import time
import json

base_dir = "/home/jose/Programming/aiml/Data/houston-AQI-weather/data/"

with open("data/coords.json") as a: coords = json.load(a)
with open("data/API_keys.json") as b: keys = json.load(b)

WWO_API = keys['WWO_API']

def get_weather(lat, long, date):
    return 'http://api.worldweatheronline.com/premium/v1/past-weather.ashx?key={key}&q={lat},{long}&format=json&date={date}&show_comments=no&tp=24' \
        .format(lat=lat, long=long, date=date, key=WWO_API)

'''
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

for name, coord in reversed(coords.items()):
    lat, long = round(coord[0], 4), round(coord[1], 4)

    name = name.replace('/', '-')
    try:
        df = pd.read_csv("/home/jose/Programming/aiml/Data/houston-AQI-weather/filled-in-data/" + name + ".csv")
    except FileNotFoundError:
        df = pd.read_csv(base_dir + name + '.csv')
        del df['sky_ceiling_height']
    del df['Unnamed: 0']


    for i in range(len(df)):
        if any((pd.isna(df[label].values[i]) or df[label].values[i] == 'NaN' or df[label].values[i] == 'NV') for label in list(df.columns[2:])):
            response_weather = requests.get(get_weather(lat, long, df.Date.values[i]))

            print(response_weather)

            try:
                if (pd.isna(df.air_temp.values[i]) or df.air_temp.values[i] == 'NaN' or df.air_temp.values[i] == 'NV'):
                    df.air_temp.values[i] = int(response_weather.json()['data']['weather'][0]['maxtempC'])
                
                if (pd.isna(df.dew_point_temp.values[i]) or df.dew_point_temp.values[i] == 'NaN' or df.dew_point_temp.values[i] == 'NV'):
                    df.dew_point_temp.values[i] = int(response_weather.json()['data']['weather'][0]['hourly'][0]['DewPointC'])

                if (pd.isna(df.sea_level_pressure.values[i]) or df.sea_level_pressure.values[i] == 'NaN' or df.sea_level_pressure.values[i] == 'NV'):
                    df.sea_level_pressure.values[i] = int(response_weather.json()['data']['weather'][0]['hourly'][0]['pressure'])

                if (pd.isna(df.visibility.values[i]) or df.visibility.values[i] == 'NaN' or df.visibility.values[i] == 'NV'):
                    df.visibility.values[i] = float(response_weather.json()['data']['weather'][0]['hourly'][0]['visibility']) * 1000

                if (pd.isna(df.wind_speed.values[i]) or df.wind_speed.values[i] == 'NaN' or df.wind_speed.values[i] == 'NV'):
                    df.wind_speed.values[i] = float(response_weather.json()['data']['weather'][0]['hourly'][0]['windspeedKmph']) / 3.2
            except KeyError:
                print('Bad data, skipping...')

            print(df.loc[[i]])

            time.sleep(1)
        df.to_csv("/home/jose/Programming/aiml/Data/houston-AQI-weather/filled-in-data/" + name + ".csv")

    print(df.head(5))