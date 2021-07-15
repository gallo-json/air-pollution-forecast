import io
import json
import requests
from bs4 import BeautifulSoup

with open("data/coords.json") as a: coords = json.load(a)
url = "https://www.tceq.texas.gov/cgi-bin/compliance/monops/peak_monthly.pl?override"

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

            while f[start_idx].strip().isdigit() or f[start_idx].strip() == 'NA':
                arr.append(int(f[start_idx]) if f[start_idx].strip().isdigit() else 'NA')
                start_idx += 3
            
            print(region_name, arr)