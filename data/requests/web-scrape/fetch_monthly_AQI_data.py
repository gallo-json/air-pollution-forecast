# Script to webscrape the reliable monthly AQI data from the TCEQ website
# Run manually to catch up with reliable data or schedule monthly
# Data is from here: https://www.tceq.texas.gov/cgi-bin/compliance/monops/peak_monthly.pl?override
# Usage (append pipe): python3 fetch_monthly_AQI_data.py >> AQI_data.csv

import io
import json
import requests
from datetime import datetime
from bs4 import BeautifulSoup

with open("data/coords.json") as a: coords = json.load(a) # Load regions and respective coordinates

# URL that will be scraped
url = "https://www.tceq.texas.gov/cgi-bin/compliance/monops/peak_monthly.pl?override"
d = datetime.now()

# Get the URL's HTML
r = requests.get(url)
soup = BeautifulSoup(r.text, features='html.parser') # Let bs4 parse the HTML
f = io.StringIO(soup.prettify()).readlines() # Beatify the HMTL (indent, etc.) and treat it as a file

# The URL's HTML is a giant mess, over 8000 lines long. Full of nests in nests
# By treating the HTML not as a real HTML but as a lined file it makes it much easier to find and select data
# Unorthodox method, maybe not best practice but works
for num, line in enumerate(f):
    for region_name, _ in coords.items():
        arr = []
        if line.strip() == region_name:
            # The first AQI value is 7 or 12 lines away from when the region name is mentioned
            if f[num + 7].strip().isdigit() or f[num + 7].strip() == 'NA':
                start_idx = num + 7
            elif f[num + 12].strip().isdigit() or f[num + 12].strip() == 'NA':
                start_idx = num + 12

            # Loop for how many days have past in this current month
            for day in range(int(d.strftime('%d')) - 1):
                line_num = start_idx + day * 3 # The AQI value appears every 3 lines from the start
                arr.append(int(f[line_num]) if f[line_num].strip().isdigit() else 'NA')
            
            # Printing then appending from bash is easier than writing to a csv using pandas
            print(d.strftime("%m-%Y") + ',' + region_name + ',1,Reg,', end='')
            print(*arr, sep = ',')