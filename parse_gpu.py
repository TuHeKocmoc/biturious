from bs4 import BeautifulSoup
import requests


def parse():
    URL = 'https://www.kryptex.org/ru/best-gpus-for-mining'
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) \
        Chrome/92.0.4515.131 YaBrowser/21.8.0.1967 (beta) Yowser/2.5 Safari/537.36'
    }
    response = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    items = soup.findAll('tr', class_='tr-link cursor-pointer')
    gpues = []
    for item in items[:5]:
        gpues.append({
            'title': item.find('a', class_='tr-link__link').get_text(strip=True)
        })

    prices = []
    for item in items[:5]:
        prices.append({
            'title': item.find('td', class_='text-center').get_text(strip=True)
        })

    gpu_and_price = [gpues[i]['title'] + ' - ' + prices[i]['title'] for i in range(5)]

    return gpu_and_price
