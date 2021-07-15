# Script to webscrape the reliable monthly AQI data from the TCEQ website
# Run manually to catch up with reliable data or schedule monthly
# 
# Usage (append pipe): python3 fetch_monthly_AQI_data.py >> AQI_data.csv

import io
import json
import requests
from datetime import datetime
from bs4 import BeautifulSoup

with open("data/coords.json") as a: coords = json.load(a)
url = "https://www.tceq.texas.gov/cgi-bin/compliance/monops/peak_monthly.pl?override"
d = datetime.now()

r = requests.get(url)
soup = BeautifulSoup(r.text, features='html.parser')
f = io.StringIO(soup.prettify()).readlines()

for num, line in enumerate(f):
    for region_name, _ in coords.items():
        arr = []
        if line.strip() == region_name:
            if f[num + 7].strip().isdigit() or f[num + 7].strip() == 'NA':
                start_idx = num + 7
            elif f[num + 12].strip().isdigit() or f[num + 12].strip() == 'NA':
                start_idx = num + 12

            for day in range(int(d.strftime('%d')) - 1):
                line_num = start_idx + day * 3
                arr.append(int(f[line_num]) if f[line_num].strip().isdigit() else 'NA')
            
            print(d.strftime("%m-%Y") + ',' + region_name + ',1,Reg,', end='')
            print(*arr, sep = ',')