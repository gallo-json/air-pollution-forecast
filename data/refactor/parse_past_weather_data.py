# NOAA dolt data
'''
    import pandas as pd
    from scipy import spatial
    import json

    with open("../coords.json") as f: coords = json.load(f)

    base_dir = "/home/jose/Programming/aiml/Data/houston-AQI-weather/"

    noaa_df = pd.read_csv(base_dir + "noaa_stations.csv")

    noaa_coords = noaa_df[['latitude', 'longitude']].to_numpy()

    noaa = []

    for name, coord in coords.items():
        tree = spatial.KDTree(noaa_coords)
        idx = int(tree.query([coord])[1])

        print(name, '->', noaa_df['name'].values[idx])
        noaa.append(noaa_df['station'].values[idx])

    for i in list(set(noaa)):
        print('"' + str(i) + '", ', end='')
'''
import os
from tqdm import tqdm

stations = ["72242712975", "72252712976", "72254312977", "99737099999", "72061700208", "99848199999", "72242953910", "72244012918", "72242012923", "72059400188", "99736199999"]

indexes = ["_air_temp", "_dew_point_temp", "_sea_level_pressure", "_sky_ceiling_height", "_visibility", "_wind_speed"]

os.chdir("/media/jose/SAMSUNG/noaa")

for s in stations:
    print(s)
    os.mkdir(s)

    for i in tqdm(indexes):
        os.system("dolt sql -r csv -q 'SELECT * FROM dolt_history" + i + " WHERE station in (\"" + s + "\")' > " + s + "/" + s + i + ".csv")
        print('Done with', i)