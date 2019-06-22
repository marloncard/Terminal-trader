import requests

APIURL = "http://dev.markitondemand.com/Api/v2/Quote/json?symbol={ticker}"

FAKEDATA = {
        "stok": 3.50
        }

def get_price(ticker):
    if ticker in FAKEDATA:
        return FAKEDATA[ticker]
    
    response = requests.get(APIURL.format(ticker=ticker))
    if response.status_code == 200:
        data = response.json()
        if data.get("Status") == "SUCCESS":
            return data["LastPrice"]
        else:
            return None
    return None