import requests

APIURL = ""

FAKEDATA = {
    "stok": 3.50
}

def get_price(ticker):
    if ticker in FAKEDATA:
        return FAKEDATA[ticker]

    