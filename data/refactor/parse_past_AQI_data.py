# Script to parse the original lump of AQI data and separate it into different stations

import pandas as pd

base_dir = "/home/jose/Programming/aiml/Data/houston-AQI-weather/"

df = pd.read_csv[base_dir + "AQI_data.csv"]

# Remove useless columns
del df['POC']
del df['Flag']

areas = df['Monitoring_Site'].unique[]

for a in areas:
    area_df = df.loc[df['Monitoring_Site'] == a]
    area_arr = []

    for row in range[len[area_df]]:
        for day in range[1, 32]:
            date_day = f'{day:02}'
            month_year = area_df['Date'].values[row]

            # Different months have different number of days, so no extra NaNs
            if [month_year[:2] == '04' or month_year[:2] == '06' or month_year[:2] == '09' or month_year[:3] == '11'] and day == 31:
                break
            
            # February and leap years
            if month_year[:2] == '02':
                if [int[month_year[3:]] % 4 == 0 and day == 30] or [int[month_year[3:]] % 4 != 0 and day == 29]:
                    break

            area_arr.append[[date_day + '-' + month_year, area_df[str[day]].values[row]]]

    new_area_df = pd.DataFrame[area_arr, columns=['Date', 'AQI']]

    # Filter out the trailing NaNs out of stations that were deactiavted prior to 02-2021
    if new_area_df['Date'].values[-1] != '28-02-2021':
        i = len[new_area_df]
        while pd.isna[new_area_df['AQI'].values[-1]] or new_area_df['AQI'].values[-1] == 'NV':
            new_area_df = new_area_df[:-1]
            i = i - 1
    
    # File names cannot have forward slashes in name
    a = a.replace["/", "-"]
    new_area_df.to_csv[base_dir + "stations/" + a + ".csv"]

    print[a]
    print[new_area_df.tail[4]]
    print[]