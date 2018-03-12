import json
import requests
import time
import matplotlib.pyplot as plt
from sklearn import datasets, linear_model
import numpy as np
from scipy import stats
from operator import itemgetter
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter, AutoMinorLocator)


# Preferences
symbol = "ETHBTC"
interval = "1m"

# 1 day = 86400 seconds
endTime = int(round(time.time() * 1000))  # ---- millisecond timestamp unix
#print endTime

startTime = endTime - 86400000  # 1 day in milliseconds
#print startTime

#  endTime is present, startTime is past

address_two = "https://api.binance.com/api/v1/klines?symbol=%s&interval=%s" %  \
        (symbol, interval)

address = "https://api.binance.com/api/v1/klines?symbol=%s&interval=%s&startTime=%s&endTime=%s" %  \
        (symbol, interval, startTime, endTime)

one_day = requests.get(address)
one_day_dict = json.loads(one_day.content)
#print one_day_dict[1]

# --- CATALOGING ---

counter = 0
ts_price = []

for w in one_day_dict:
    column = []
    ts_price.append(column)

    ts_price[counter].append(one_day_dict[counter][0])
    ts_price[counter].append(one_day_dict[counter][4])
    counter += 1

#print ts_price
#print ts_price[1][0]

# sorting of all timestamps and prices for full graph
all_timestamps = []
all_prices = []
hexagon = 0
for u in ts_price:
    all_timestamps.append(ts_price[hexagon][0])
    all_prices.append(ts_price[hexagon][1])
    hexagon += 1


# --- SORTING ---


ts_price_high = sorted(ts_price, key=itemgetter(1), reverse=True)  # sorted by highest price first
#print ts_price_high

ts_price_high_top = []
h = 0
for h in range(0, 5):  # top n prices and equivalent timestamps
    ts_price_high_top.append(ts_price_high[h])
    h += 1
#print ts_price_high_top

# HIGHEST above, LOWEST below

ts_price_low = sorted(ts_price, key=itemgetter(1))  # sorted by lowest price first
#print ts_price_low

ts_price_low_top = []
m = 0
for m in range(0, 5):  # lowest n prices and equivalent timestamps
    ts_price_low_top.append(ts_price_low[m])
    m += 1
#print ts_price_low_top

# SORTING TIMESTAMPS FOR ACCURATE GRAPHING
ts_price_high_sts = sorted(ts_price_high_top, key=itemgetter(0), reverse=True)  # sorted by timestamp value / highest
ts_price_low_sts = sorted(ts_price_low_top, key=itemgetter(0), reverse=True)  # same as above


ts_high_sorted = []
ts_low_sorted = []
n = 0
for n in range(0, 5):
    ts_high_sorted.append(ts_price_high_sts[n][0])
    ts_low_sorted.append(ts_price_low_sts[n][0])
    n += 1

price_high = []  # sorted by timestamps value
price_low = []   # sorted by timestamps value
o = 0
for o in range(0, 5):
    price_high.append(ts_price_high_sts[o][1])
    price_low.append(ts_price_low_sts[o][1])
    o += 1


# --- GRAPHING --- endTime & startTime

# majorLocator = MultipleLocator(float(1000000))
# majorFormatter = FormatStrFormatter('%2.2e')
# minorLocator = MultipleLocator(5)

# x_high = np.array(ts_high_sorted)
# y_high = np.array(price_high)
# x_low = np.array(ts_low_sorted)
# y_low = np.array(price_low)
# x_all = np.array(all_timestamps)
# y_all = np.array(all_prices)
#
# all_top_timestamps = ts_high_sorted + ts_low_sorted
# print min(all_top_timestamps)
# print max(all_top_timestamps)
#
# fig, ax = plt.subplots()
# ax.plot(x_low, y_low, 's')
# ax.plot(x_high, y_high, 'ro')
# ax.plot(x_all, y_all)

# ax.xaxis.set_major_locator(majorLocator)
# ax.xaxis.set_major_formatter(majorFormatter)
#
# # for the minor ticks, use no labels; default NullFormatter
# ax.xaxis.set_minor_locator(minorLocator)


#plt.xticks(min(all_timestamps), max(all_timestamps)+60, 60)

# plt.show()


x_one = np.array(ts_high_sorted).astype(np.float)
y_one = np.array(price_high).astype(np.float)

x_two = np.array(ts_low_sorted).astype(np.float)
y_two = np.array(price_low).astype(np.float)

print x_one
print y_one

slope_one, intercept_one, r_value_one, p_value_one, std_err_one = stats.linregress(x_one, y_one)
slope_two, intercept_two, r_value_two, p_value_two, std_err_two = stats.linregress(x_two, y_two)


#print slope_one, intercept_one
#print slope_two, intercept_two

#plt.plot(x_one, y_one, 'o', label='high prices')
#plt.plot(x_one, intercept_one + slope_one*x_one, 'r', label='high price line')
#plt.plot(x_two, y_two, 's', label='low prices')
#plt.plot(x_two, intercept_two + slope_two*x_two, 'b-', label='low price line')
#plt.legend()
#plt.show()


#########################################################
#   1499040000000, // Open time         0
#   "0.01634790", // Open               1
#   "0.80000000", // High               2
#   "0.01575800", // Low                3
#   "0.01577100", // Close              4
#   "148976.11427815", // Volume
#   1499644799999, // Close time
#   "2434.19055334", // Quote asset volume
#   308, // Number of trades
#   "1756.87402397", // Taker buy base asset volume
#   "28.46694368", // Taker buy quote asset volume
#   "17928899.62484339" // Ignore
#########################################################
