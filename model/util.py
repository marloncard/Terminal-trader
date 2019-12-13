import requests
import pathlib

BASE_URL = "https://cloud.iexapis.com"
ENDPOINT = "/stable/tops?token={token}&symbols={symbol}"

with open('{home}/.credentials/IEXTOKEN.txt'.format(home=pathlib.Path.home())) as f:
    TOKEN = f.read().strip()

FAKEDATA = {
        "stok": 3.50
        }

def get_price(ticker):
    if ticker in FAKEDATA:
        return FAKEDATA[ticker]
    url = BASE_URL + ENDPOINT.format(symbol=ticker, token=TOKEN)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data:
                return data[0]["lastSalePrice"]
            else:
                return None
        else:
            return None
    except requests.RequestException as e:
        print("Connection Error: ", e)
        return None


if __name__ == '__main__':
    print(get_price('pfe'))