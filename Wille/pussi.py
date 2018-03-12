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


# Writes data to csv file
#def write_to_file(priceList, result):


# Calculating wedges, 0=Rising 1=Falling 2=No wedge
def wedge_calc(slope_high, slope_low):
    if slope_high > 0 and slope_low > 0 and slope_high < slope_low:     # Rising wedge
        return 0
    elif slope_high < 0 and slope_low < 0 and slope_high < slope_low:   # Falling wedge
        return 1
    else:
        return 2

# Used to retrieve all elements at index n in nested list list
def get_subList(list, n):
    newList = []
    for x in list:
        newList.append(x[n])
    return newList

# Calculate wedges. Returns a list containing two list, each holding wedge data
def get_wedges(sortedClosePrices):

    # Sort close prices and split into highest and lowest
    lows = sortedClosePrices[0:(interval/2)]
    highs = sortedClosePrices[interval/2:interval]

    # Construct lists for regression
    x_high = np.array(get_subList(highs, 0)).astype(np.float)
    y_high = np.array(get_subList(highs, 1)).astype(np.float)
    x_low = np.array(get_subList(lows, 0)).astype(np.float)
    y_low = np.array(get_subList(lows, 1)).astype(np.float)

    # Linear regression to form wedges
    slope_high, intercept_high, r_value_high, p_value_high, std_err_high = stats.linregress(x_high, y_high)
    slope_low, intercept_low, r_value_low, p_value_low, std_err_low = stats.linregress(x_low, y_low)

    #plot_wedges(x_low, y_low, intercept_low, slope_low, x_high, y_high, intercept_high, slope_high)

    return wedge_calc(slope_high, slope_low)

# Plots wedges
def plot_wedges(x_low, y_low, intercept_low, slope_low, x_high, y_high, intercept_high, slope_high):
    plt.plot(x_high, y_high, 'o', label='high prices')
    plt.plot(x_high, intercept_high + slope_high*x_high, 'r', label='high price line')
    plt.plot(x_low, y_low, 's', label='low prices')
    plt.plot(x_low, intercept_low + slope_low*x_low, 'b-', label='low price line')
    plt.legend()
    plt.show()

# Determines bull/bear for coming epok
def is_bull(nextEpok, currentHigh):
    nextEpokPrices = []
    for date in nextEpok:
        currentClosePrice = float(nextEpok[date]["4. close"])
        nextEpokPrices.append(float(currentClosePrice))

    sortedNextEpokPrices = sorted(nextEpokPrices)
    nextEpokHighest = sortedNextEpokPrices[len(sortedNextEpokPrices)-1]
    nextEpokLowest = sortedNextEpokPrices[0]

    if nextEpokHighest < currentHigh:
        return False
    else:
        if abs(nextEpokHighest-currentHigh) > abs(currentHigh-nextEpokLowest):
            return True
        else:
            return False

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


finalData = []
counter = 0

# Iterate over each epok containing 5 dictionaries
for epok in epoks:

    # List of all close prices in current epok
    closePrices = []

    # Iterate over each dictionary within epok
    for date in epok:
        currentClosePrice = float(epok[date]["4. close"])

        # Convert time to UNIX time
        unixTime = datetime.datetime.strptime(date, '%Y-%m-%d').strftime("%s")
        closePrices.append([unixTime, float(currentClosePrice)])

    sortedClosePrices = sorted(closePrices, key=itemgetter(1))
    currentEpokHighest = sortedClosePrices[len(sortedClosePrices)-1][1]

    # Only use epok if RAISING wedge exists
    if get_wedges(sortedClosePrices) == 0:

        # Check if current wedge leads to higher or lower price next epok
        nextEpok = epoks[counter+1]
        if is_bull(nextEpok, currentEpokHighest):
            finalData.append([np.array(sortedClosePrices)[:,1].tolist(), 1])
        else:
            finalData.append([np.array(sortedClosePrices)[:,1].tolist(), 0])

    counter += 1

print len(finalData)
