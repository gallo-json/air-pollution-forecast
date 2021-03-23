import pandas as pd
import numpy as np
from scipy import spatial
import json

with open("data/coords.json") as f: coords = json.load(f)

base_dir = "/home/jose/Programming/aiml/Data/houston-AQI-weather/"

noaa_df = pd.read_csv(base_dir + "noaa_stations.csv")

noaa_coords = noaa_df[['latitude', 'longitude']].to_numpy()

for tceq_name, tceq_coord in coords.items():
    tree = spatial.KDTree(noaa_coords)
    idx = int(tree.query([tceq_coord])[1])

    noaa_station =  noaa_df['station'].values[idx]
    #print(tceq_name, '->', noaa_station)

    tceq_name = tceq_name.replace('/', '-')
    tceq_station_df = pd.read_csv(base_dir + "stations/" + tceq_name + ".csv")
    del tceq_station_df['Unnamed: 0']

    first_day = tceq_station_df['Date'].values[0]
    last_day = tceq_station_df['Date'].values[-1]

    tceq_station_df['Date'] = pd.to_datetime(tceq_station_df['Date'], errors='coerce', format='%d-%m-%Y')

    for label in ["air_temp", "dew_point_temp", "sea_level_pressure", "sky_ceiling_height", "visibility", "wind_speed"]:
        label_df = pd.read_csv("/media/jose/SAMSUNG/noaa/" + str(noaa_station) + "/" + str(noaa_station) + "_" + label + ".csv")

        del label_df['commit_hash']
        del label_df['committer']

        label_df['commit_date'] = pd.to_datetime(label_df['commit_date'], errors='coerce', format='%Y-%m-%d 00:00:00 +0000 UTC')
        label_df = label_df[label_df.commit_date.isin(tceq_station_df.Date.values)]
        label_df = label_df.sort_values(by=['commit_date'])

        assert len(label_df) <= len(tceq_station_df)

        start_diff = len(tceq_station_df)
        end_diff = 0

        if len(label_df) != 0:
            start_diff = tceq_station_df.loc[tceq_station_df.Date == label_df.commit_date.values[0]].index[0]
            end_diff = len(tceq_station_df) - start_diff - len(label_df)

        label_arr = (['NaN'] * start_diff) + list(label_df['avg']) + (['NaN'] * end_diff)

        tceq_station_df[label] = label_arr

    print(tceq_station_df.head(5))
    tceq_station_df.to_csv(base_dir + 'data/' + tceq_name + '.csv')
    