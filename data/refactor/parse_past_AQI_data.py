import pandas as pd

df = pd.read_csv("/home/jose/Programming/aiml/Data/houston-AQI-weather/AQI_data.csv")

# Remove useless columns
del df['POC']
del df['Flag']

areas = df['Monitoring_Site'].unique()

for a in areas:
    area_df = df.loc[df['Monitoring_Site'] == a]
    area_arr = []

    for row in range(len(area_df)):
        for day in range(1, 32):
            date_day = f'{day:02}'
            month_year = area_df['Date'].values[row]

            if (month_year[:2] == '04' or month_year[:2] == '06' or month_year[:2] == '09' or month_year[:3] == '11') and day == 31:
                break

            if month_year[:2] == '02':
                if (int(month_year[3:]) % 4 == 0 and day == 30) or (int(month_year[3:]) % 4 != 0 and day == 29):
                    break

            area_arr.append([date_day + '-' + month_year, area_df[str(day)].values[row]])

    new_area_df = pd.DataFrame(area_arr, columns=['Date', 'AQI'])

    print(a)
    print(new_area_df.head(4))
    print()