import json
from pprint import pprint
import requests
from bs4 import BeautifulSoup
with open('css_selectors.json', 'r') as mappings:
    css_maps = json.load(mappings)

r = requests.get('https://occovid19.ochealthinfo.com/coronavirus-in-oc')
if r.status_code == 200:
    print('successful request')
    html = r.text
    soup = BeautifulSoup(''.join(html), 'html.parser')
    # print('--- Whole Soup ---') 
    # print(soup.prettify())
    # print('---- Scripts ----')
    # print(soup.findAll('script'))
    data = {}
    for key, selector in css_maps.items():
        try:
            data[key]  = soup.select_one(selector).text
        except Exception as e:
            print(key)
            print(str(e))
    table = soup.find("table").find("tbody")
    try:
        rows = table.find_all('tr')
        for row in rows:
            cells = row.find_all('td')
            city = cells[0].text
            data[city] = {}
            data[city]['population'] = cells[1].text
            data[city]['cases'] = cells[2].text
    except Exception as e:
        print(str(e))

    pprint(data)


else:
    print('could not access site')
    print(r.status_code)
