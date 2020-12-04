import requests
from bs4 import BeautifulSoup
import re


def get_promoted_cars():
    site_url = "https://www.autovit.ro"
    page = requests.get(site_url)
    soup = BeautifulSoup(page.content, "html.parser")
    promoted_cars = soup.find_all('section', class_='css-12rnw22 e64f3h70')
    for cars in promoted_cars:
        name = cars.find('h3', class_='css-mf3iot css-10hph01 e1q5tycg0')
        price = cars.find('div', class_='css-13aaiz8 css-7tvyk6 e1ptxbj01')
        for i in cars.find_all('span', class_='css-12tzx1b'):
            match = re.match(r'.*([1-2][0-9]{3})', i.text)
            if match is not None:
                year = match.group(1)
            if i.text.endswith('km'):
                odometer = i.text
        print(name.text.strip())
        print(price.text.strip())
        print(year)
        print(odometer)


if __name__ == '__main__':
    get_promoted_cars()
