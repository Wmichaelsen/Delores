import requests
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import datetime
from operator import itemgetter

#---- CONSTANTS ----
API_KEY = "EBHYLXXG3AQGI8XN"

# Epok interval. This is the time frame in which wedges will be calculated
interval = 6

candleStickInterval = 1

#---- HELPER FUNCTIONS ----

# Used to retrieve all elements at index n in nested list list
def getSubList(list, n):
    newList = []
    for x in list:
        newList.append(x[n])
    return newList

# Plots wedges
def plotWedges(x_low, y_low, intercept_low, slope_low, x_high, y_high, intercept_high, slope_high):
    plt.plot(x_high, y_high, 'o', label='high prices')
    plt.plot(x_high, intercept_high + slope_high*x_high, 'r', label='high price line')
    plt.plot(x_low, y_low, 's', label='low prices')
    plt.plot(x_low, intercept_low + slope_low*x_low, 'b-', label='low price line')
    plt.legend()
    plt.show()

#---- DATA GATHERING ----
r = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=GOOG&outputsize=full&apikey='+API_KEY)

if r.status_code != requests.codes.ok:
    print "Bad request"

myJSON = r.json()

# Original stock data object
stockData = myJSON["Time Series (Daily)"]

# Takes stockData and sorts all keys (the dates) and store them in array for later use
sortedStockDataKeys = sorted(stockData.keys(), key=lambda d: map(int, d.split("-")))


#---- DATA STRUCTURING (FORMING EPOKS) ----
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


#---- WEDGE CONSTRUCTION ----

# Iterate over each epok containing 5 dictionaries
for epok in epoks[0:1]:

    # List of all close prices in current epok
    closePrices = []

    # Iterate over each dictionary within epok
    for date in epok:
        currentClosePrice = epok[date]["4. close"]

        # Convert time to UNIX time
        unixTime = datetime.datetime.strptime(date, '%Y-%m-%d').strftime("%s")
        closePrices.append([unixTime, currentClosePrice])

    # Sort close prices and split into highest and lowest
    sortedClosePrices = sorted(closePrices, key=itemgetter(1))
    lows = sortedClosePrices[0:(interval/2)]
    highs = sortedClosePrices[interval/2:interval]

    x_high = np.array(getSubList(highs, 0)).astype(np.float)
    y_high = np.array(getSubList(highs, 1)).astype(np.float)
    x_low = np.array(getSubList(lows, 0)).astype(np.float)
    y_low = np.array(getSubList(lows, 1)).astype(np.float)

    # Linear regression to form wedges
    slope_high, intercept_high, r_value_high, p_value_high, std_err_high = stats.linregress(x_high, y_high)
    slope_low, intercept_low, r_value_low, p_value_low, std_err_low = stats.linregress(x_low, y_low)

    #plotWedges(x_low, y_low, intercept_low, slope_low, x_high, y_high, intercept_high, slope_high)

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
