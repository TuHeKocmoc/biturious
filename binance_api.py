from binance.client import Client
import pathlib
import os

path = str(pathlib.Path(__file__).parent.resolve()) + '\settings.txt'
if os.path.exists(self.path):
    file = open(path, 'r')
    data = file.readlines()
else:
    data = ['', '', '', '']
apikey = ' '
secretkey = ''

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
