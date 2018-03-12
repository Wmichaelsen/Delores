import requests
from scipy import stats
import numpy as np

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

x_one = np.array(DICTIONARY).astype(np.float)
y_one = np.array(DICTIONARY).astype(np.float)

x_two = np.array(DICTIONARY).astype(np.float)
y_two = np.array(DICTIONARY).astype(np.float)

above_slope, intercept_above, r_value_above, p_value_above, std_err_above = stats.linregress(x_one, y_one) # highest values
below_slope, intercept_below, r_value_below, p_value_below, std_err_below = stats.linregress(x_two, y_two)


if above_slope > 0 and below_slope > 0 and above_slope < below_slope:  # Rising wedge
    print "Rising wedge"


elif above_slope < 0 and below_slope < 0 and above_slope < below_slope:  # Falling wedge
    print "Falling wedge"

else:
    print "No wedge found"

