import requests

API_KEY = "EBHYLXXG3AQGI8XN"

r = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=GOOG&outputsize=full&apikey='+API_KEY+'&dataType=CSV')

if r.status_code != requests.codes.ok:
    print "Bad request"

myJSON = r.json()
stockData = myJSON["Time Series (Daily)"]

interval = 7
candleStickInterval = 1

for key in stockData



#---- Wedge calculator -----
# Undre har storre k-varde an ovre
# above_slope is the five highest values
# below_slope is the five lowest values

# if above_slope > 0 and below_slope > 0 and above_slope < below_slope:  # Rising wedge
#     print "Rising wedge"
#
# elif above_slope < 0 and below_slope < 0 and above_slope < below_slope:  # Falling wedge
#     print "Falling wedge"
#
# else:
#     print "No wedge found"

