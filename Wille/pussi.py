import requests
API_KEY = "EBHYLXXG3AQGI8XN"

r = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=GOOG&outputsize=full&apikey='+API_KEY)

if r.status_code != requests.codes.ok:
    print "Bad request"

myJSON = r.json()

# Original stock data object
stockData = myJSON["Time Series (Daily)"]

# Takes stockData and sorts all keys (the dates) and store them in array for later use
sortedStockDataKeys = sorted(stockData.keys(), key=lambda d: map(int, d.split("-")))

# Epok interval. This is the time frame in which wedges will be calculated
interval = 5

candleStickInterval = 1

# First data point in stockData
firstKey = stockData.keys()[0]
firstDate = int(firstKey.split("-")[2])

epoks = []
epok = {}

counter = 0
for dateKey in sortedStockDataKeys:
    if counter < interval:
        epok[dateKey] = stockData[dateKey]
        counter += 1
    else:
        epoks.append(epok)
        epok = {}
        counter = 0

print len(epoks)
