from bs4 import BeautifulSoup
import requests


def parse():
    URL = 'https://ru.investing.com/crypto/bitcoin/btc-usd'
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) \
        Chrome/92.0.4515.131 YaBrowser/21.8.0.1967 (beta) Yowser/2.5 Safari/537.36'
    }
    response = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    items = soup.findAll('div', class_='wrapper')
    price = ''
    for i in items:
        price = {
            'title': i.find('span', class_='arial_26 inlineblock pid-945629-last').get_text(strip=True)
        }
    return f"Курс биткоина: {price['title']} $"
