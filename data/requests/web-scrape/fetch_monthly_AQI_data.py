import requests
from bs4 import BeautifulSoup

url = "https://www.tceq.texas.gov/cgi-bin/compliance/monops/peak_monthly.pl?override"

r = requests.get(url)
soup = BeautifulSoup(r.text, features='html.parser')

print(soup.prettify())