# NOAA dolt data

import pandas as pd
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

    for label in ["air_temp", "dew_point_temp", "sea_level_pressure", "sky_ceiling_height", "visibility", "wind_speed"]:
        label_df = pd.read_csv("/media/jose/SAMSUNG/noaa/" + str(noaa_station) + "/" + str(noaa_station) + "_" + label + ".csv")

        # Filter out years before 1997
        label_df = label_df[(label_df['commit_date'].str[:4]).map(int) >= 1997]

        print(label_df.head(5))
        print()