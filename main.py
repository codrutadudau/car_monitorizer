import requests
from bs4 import BeautifulSoup
import re
import json
import time
import os

site_url = "https://www.autovit.ro"
page = requests.get(site_url)
soup = BeautifulSoup(page.content, "html.parser")


def get_promoted_cars():
    promoted_cars = soup.find_all('section', class_='css-12rnw22 e64f3h70')
    feeds = []
    for cars in promoted_cars:
        name = cars.find('h3', class_='css-mf3iot css-10hph01 e1q5tycg0')
        price = cars.find('div', class_='css-13aaiz8 css-7tvyk6 e1ptxbj01')
        for i in cars.find_all('span', class_='css-12tzx1b'):
            match = re.match(r'.*([1-2][0-9]{3})', i.text)
            if match is not None:
                year = match.group(1)
            if i.text.endswith('km'):
                odometer = i.text
        car = {
            'name': name.text,
            'price': price.text,
            'year': year,
            'odometer': odometer
        }
        feeds.append(car)
    return feeds


def deal_of_the_day():
    offer = soup.find('section', class_='css-1i4x0sm e64f3h70')
    feed = []
    name = offer.find('h3', 'css-mf3iot css-10hph01 e1q5tycg0')
    price = offer.find('div', class_='css-13aaiz8 css-7tvyk6 e1ptxbj01')
    for i in offer.find_all('span', class_='css-12tzx1b'):
        match = re.match(r'.*([1-2][0-9]{3})', i.text)
        if match is not None:
            year = match.group(1)
        if i.text.endswith('km'):
            odometer = i.text
    daily_offer = {
        'name': name.text,
        'price': price.text,
        'year': year,
        'odometer': odometer
    }
    feed.append(daily_offer)
    return feed


def json_file():
    feeds = get_promoted_cars()
    feed = deal_of_the_day()
    result = feeds + feed
    file_path = "output.json"
    if os.stat(file_path).st_size == 0:
        with open(file_path, 'w') as f:
            json.dump(result, f, indent=4)
    else:
        with open(file_path, 'r') as f:
            data = json.load(f)
        with open(file_path, 'w') as f:
            data.append(result)
            json.dump(data, f, indent=4)


if __name__ == '__main__':
    while True:
        json_file()
        time_wait = 3600*24
        print(f"Waiting {time_wait} seconds... ")
        time.sleep(time_wait)
