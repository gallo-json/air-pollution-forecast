import pandas as pd

df = pd.read_csv("/home/jose/Programming/aiml/Data/houston-AQI-weather/AQI_data.csv")

# Remove useless columns
del df['POC']
del df['Flag']

areas = df['Monitoring_Site'].unique()