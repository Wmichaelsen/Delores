import requests

# Wille is a little pussy
API_KEY = "EBHYLXXG3AQGI8XN"

r = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=GOOG&outputsize=full&apikey='+API_KEY+'&dataType=CSV')

if r.status_code != requests.codes.ok:
    print "Bad request"

myJSON = r.json()
stockData = myJSON["Time Series (Daily)"]

interval = 7
candleStickInterval = 1

for key in stockData
