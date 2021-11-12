from binance.client import Client
import pathlib

path = str(pathlib.Path(__file__).parent.resolve()) + '\settings.txt'
file = open(path, 'r')
data = file.readlines()
try:
    apikey = data[2].strip()
    apikey = apikey[apikey.find('=') + 1:]
    secretkey = data[3].strip()
    secretkey = secretkey[secretkey.find('=') + 1:]
except:
    apikey = ' '
    secretkey = ''

client = Client(
    apikey,
    secretkey
)