# NOAA dolt data

import pandas as pd

stations = [
    72059400188,
72061700208,
72063700223,
72242712975,
72243012960,
72243612906,
72244012918,
72252712976,
72254312977,
99848199999,
72242953910,
72244453902,
72244753903,
72091700306,
72241012917,
72242012923,
99736199999,
99736499999,
99737099999,
99772999999,
99818299999
]

stations = [str(st) for st in stations]

base_dir = "/home/jose/Programming/aiml/Data/houston-AQI-weather/"

df = pd.read_csv(base_dir + "noaa_stations.csv")

df_filtered = df[df['station'].isin(stations)]

df_filtered.to_csv('noaa_stations.csv')