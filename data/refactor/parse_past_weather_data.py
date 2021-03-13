# NOAA dolt data

import pandas as pd
from scipy import spatial
import json

with open("../coords.json") as f: coords = json.load(f)

base_dir = "/home/jose/Programming/aiml/Data/houston-AQI-weather/"

noaa_df = pd.read_csv(base_dir + "noaa_stations.csv")

noaa_coords = noaa_df[['latitude', 'longitude']].to_numpy()

for name, coord in coords.items():
    tree = spatial.KDTree(noaa_coords)
    idx = int(tree.query([coord])[1])

    print(name, '->', noaa_df['name'].values[idx])