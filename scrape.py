import json
from pprint import pprint
import requests
from bs4 import BeautifulSoup
import logging
from datetime import datetime as dt
from etl import DataHandler

logger = logging.getLogger(__name__)
f_handler = logging.FileHandler('scraper.log')
f_handler.setLevel(logging.WARNING)

logger.addHandler(f_handler)

with open('css_selectors.json', 'r') as mappings:
    css_maps = json.load(mappings)

data_handler = DataHandler()

r = requests.get('https://occovid19.ochealthinfo.com/coronavirus-in-oc')
if r.status_code == 200:
    logger.info(f'successful request: {dt.now().strftime("%c")}')
    html = r.text
    soup = BeautifulSoup(''.join(html), 'html.parser')
    data = {}
    for key, selector in css_maps.items():
        try:
            data[key] = soup.select_one(selector).text
        except Exception as e:
            logger.error("exception occured", exc_info=True)
            logger.error('update selector for ' + key)
    data['timestamp'] = dt.now().strftime('%c')
    print(data)
    data_handler.append_data(data)

    table = soup.find("table").find("tbody")
    try:
        rows = table.find_all('tr')
        for row in rows:
            cells = row.find_all('td')
            city_data = {}
            city_data['city'] = cells[0].text
            city_data['population'] = cells[1].text
            city_data['cases'] = cells[2].text
            city_data['timestamp'] = dt.now().strftime('%c')
            data_handler.append_data(city_data)

        data_handler.save_data()
    except Exception as e:
        raise e
        logger.error("exception occured", exc_info=True)


else:
    logger.error(f'could not access site status code: {r.status_code}')

