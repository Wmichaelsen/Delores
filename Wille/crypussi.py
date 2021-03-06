import requests
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import datetime
from operator import itemgetter
import csv
import time
from time import sleep

#---- CONSTANTS ----


# Epok interval. This is the time frame in which wedges will be calculated
interval = 6

candleStickInterval = 1


#---- HELPER FUNCTIONS ----


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

# Writes data to CSV file
def writeDataToCSV(data, fileName):
    with open(fileName, 'a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)

def formatDate(date):
    newDate = date
    newDate = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S').strftime("%s")
    return newDate

# Loads all stock symbols from SP500 1st column
def loadStockSymbols(stocksCSV):
    with open(stocksCSV) as file:
        reader = csv.reader(file)
        stocks = list(reader)

    stockSymbols = np.array(stocks)[:,0].tolist()

    return stockSymbols

#---- MAIN FUNCTIONS ----

# Loading data for given stock
def loadData(symbol):
    endTime = int(round(time.time() * 1000))  # ---- millisecond timestamp unix
    startTime = endTime - 864000000  # Ten days in milliseconds

    adress = "https://api.binance.com/api/v1/klines?symbol=%s&interval=1m&startTime=%s&endTime=%s" %  \
        (symbol, startTime, endTime)
    r = requests.get(adress)
    if r.status_code != requests.codes.ok:
        print "Bad request"
        return 0
    print symbol
    return r.json()

# Forming epoks given stockData for specific stock
def formEpoks(stockData):
    sortedStockDataKeys = sorted(map(lambda d: formatDate(d), stockData.keys()))

    epoks = []
    epok = {}

    counter = 0
    for dateKey in sortedStockDataKeys:
        if counter < interval:
            regularTime = datetime.datetime.fromtimestamp(int(dateKey)).strftime('%Y-%m-%d %H:%M:%S')
            epok[regularTime] = stockData[regularTime]
            counter += 1
        else:
            epoks.append(epok)
            epok = {}
            counter = 0

    return epoks

# Wedge construction given epoks for specific stock
def testWedge(epoks):
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
            unixTime = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S').strftime("%s")
            closePrices.append([float(unixTime), float(currentClosePrice)])

        sortedClosePrices = sorted(closePrices, key=itemgetter(1))
        currentEpokHighest = sortedClosePrices[len(sortedClosePrices)-1][1]

        # Only use epok if RAISING wedge exists
        if get_wedges(sortedClosePrices) == 0:

            # Check if current wedge leads to higher or lower price next epok
            if counter < len(epoks)-1:
                nextEpok = epoks[counter+1]
                if is_bull(nextEpok, currentEpokHighest):
                    fin = np.append(np.array(sortedClosePrices)[:,1],int(1)).tolist()
                    finalData.append(fin)
                else:
                    fin = np.append(np.array(sortedClosePrices)[:,1],int(0)).tolist()
                    finalData.append(fin)

        counter += 1

    return finalData

def saveFinalData(finalData):
    writeDataToCSV(finalData, "finalData.csv")


#---- SUPER FUNCTION ----


# Uses all main functions defined above and saves final data to be used as input in the neural network
def collectDataForSymbol(symbol):
    sleep(20)
    stockData = loadData(symbol)
    if stockData != 0:
        epoks = formEpoks(stockData)
        finalData = testWedge(epoks)
        saveFinalData(finalData)
    else:
        print "loadData() fail. Bad request"


#---- INITIATION ----


# Will hold symbols for all S&P500 stocks
allStocks = loadStockSymbols("sp500stocks.csv")

# Maps the super function onto each stock
map(lambda d: collectDataForSymbol(d), allStocks)
