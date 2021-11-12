from binance_api import client, Client


def price(pool):
    prices = []
    if pool == 'Месяц':
        prices = client.get_historical_klines("BTCBUSD", Client.KLINE_INTERVAL_1DAY, "1 month ago UTC")
    elif pool == 'Неделя':
        prices = client.get_historical_klines("BTCBUSD", Client.KLINE_INTERVAL_1DAY, "1 week ago UTC")
    elif pool == 'День':
        prices = client.get_historical_klines("BTCBUSD", Client.KLINE_INTERVAL_1HOUR, "1 day ago UTC")
    elif pool == 'Час':
        prices = client.get_historical_klines("BTCBUSD", Client.KLINE_INTERVAL_15MINUTE, "1 hour ago UTC")

    return prices
