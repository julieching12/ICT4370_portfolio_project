"""
Author:		Fengyi
Date Created:	08/23/2020
Description:	This program has two parts:
				First part, pull data from folder .csv files for stocks data during 2015-08-03 to 
				2017-08-03, provide candlestick plot for each stock historic price trend, measure 
				their volatility by calculating their average price & standard deviations. Calculate 
				correlation coefficient for stocks to indicate their moves compared to the market(SPY).
				
				Second part is to continue analyse one specfic stock (eg GOOG) by pulling data from 
				YahooFinance, exploring its rolling mean and return rate, comparing it with one of 
				its competitor by correlation analysis. Pandas, mplfinance and matplotlib are used 
				throughout the whole analysis.
"""


# Part I: Analyze stock historic bahavior(2015-08-03 to 2017-08-03) from folder csv files

# import the libraries we need
import pandas as pd
import mplfinance as mpf
import matplotlib.pyplot as plt
import glob
import os
from datetime import datetime
from matplotlib.dates import DateFormatter, MonthLocator

# Use mplfinance to show each stock value output & trending chart
# Open, close as bar line & high low range as vertical line
path = r'C:\Python_classes\Data'
try:
	all_files = glob.glob(path + "/*.csv")
except FileNotFoundError:
	print ("No such file or directory!")
else:
	for filename in all_files:
		daily = pd.read_csv(filename, index_col=0, parse_dates=True)
		daily['Symbol'] = os.path.basename(filename.split(".")[0])
		print (daily)
		daily.index.name = 'Date'
		daily.shape
		mpf.plot(daily, type='candle', mav=(3,6,9), volume=True, datetime_format='%Y-%m', 
			ylabel='Price', ylabel_lower='Volume')
		plt.show()


# Build dataframe for pandas data analysis
path = r'C:\Python_classes\Data'
try:
	all_files = glob.glob(path + "/*.csv")
except FileNotFoundError:
	print ("No such file or directory!")
else:
	stock = []
	for filename in all_files:
		stock_df = pd.read_csv(filename, index_col = None, header = 0)
		stock_df['Symbol'] = os.path.basename(filename.split(".")[0])
		stock.append(stock_df)
	df = pd.concat(stock, axis = 0, ignore_index = True)

# Calculate stock average price and standard deviation 
open_df = df.groupby(['Symbol']).agg({'Open':['mean', 'std']})
close_df = df.groupby(['Symbol']).agg({'Close':['mean', 'std']})
merge_stats_df = pd.merge(open_df, close_df, how = 'left', on = ['Symbol'])
print(merge_stats_df)

# Build dataframe for correlation coefficient analysis
spy_path = r'C:\Python_classes\Data\SPY.csv'
spy_df = pd.read_csv(spy_path)
corr_df = pd.merge(df, spy_df, how = 'left', on = ['Date'])
corr_df.columns = [c.replace(' ', '_') for c in corr_df.columns]

# Calculate correlation coefficient for stocks compared to SPY
open_corr_df = corr_df.groupby(['Symbol']).Open_x.corr(corr_df.Open_y)
high_corr_df = corr_df.groupby(['Symbol']).High_x.corr(corr_df.High_y)
low_corr_df = corr_df.groupby(['Symbol']).Low_x.corr(corr_df.Low_y)
close_corr_df = corr_df.groupby(['Symbol']).Close_x.corr(corr_df.Close_y)
adjclose_corr_df = corr_df.groupby(['Symbol']).Adj_Close_x.corr(corr_df.Adj_Close_y)
volume_corr_df = corr_df.groupby(['Symbol']).Volume_x.corr(corr_df.Volume_y)

merge_corr_df = pd.merge(open_corr_df, high_corr_df, how = 'left', on = ['Symbol'])
merge_corr_df = pd.merge(merge_corr_df, low_corr_df, how = 'left', on = ['Symbol'])
merge_corr_df = pd.merge(merge_corr_df, close_corr_df, how = 'left', on = ['Symbol'])
merge_corr_df = pd.merge(merge_corr_df, adjclose_corr_df, how = 'left', on = ['Symbol'])
merge_corr_df = pd.merge(merge_corr_df, volume_corr_df, how = 'left', on = ['Symbol'])
print(merge_corr_df)

# Generate graph for stocks value variation
fig,ax = plt.subplots()
symbols = set(df['Symbol'])
df['Date'] = pd.to_datetime(df['Date'])
for symbol in symbols:
	ax.plot(df[df.Symbol==symbol].Date, df[df.Symbol==symbol].Close, label=symbol)
ax.xaxis.set_major_formatter(DateFormatter('%Y-%m'))
ax.xaxis.set_major_locator(MonthLocator(interval=3))
ax.set_xlabel("Date")
ax.set_ylabel("Close Price")
ax.legend()
plt.show()


# Part II: Pull 2017-08-03 to 2020-08-03 data fr YahooFinance for specific stock analysis

# Import libraries needed
import datetime
import pandas_datareader.data as web
import matplotlib.pyplot as plt
from matplotlib import style

# Adjust style of matplotlib
style.use('ggplot')

# Setup start date and end date
start = datetime.datetime(2017, 8, 3)
end = datetime.datetime(2020, 8, 3)

# Load YahooFinance Dataset for GOOG for example
df = web.DataReader("GOOG", 'yahoo', start, end)
df.tail()
print (df)

# Show Rolling Mean(Moving Average) -to determine trend
close_px = df['Adj Close']
mavg = close_px.rolling(window=100).mean()
close_px.plot(label='GOOG')
mavg.plot(label='moving avg')
plt.legend()
plt.show()

# Explore Return Deviation -risk and return
rets = close_px/close_px.shift(1) - 1
rets.plot(label='GOOG return')
plt.legend()
plt.show()

# Analyse competitors stocks (choose some you want to compare)
dfcomp = web.DataReader(['GOOG', 'MSFT', 'RDS-A', 'AIG', 'IBM', 'SPY'], 
	'yahoo', start=start, end=end)['Adj Close']
print (dfcomp)

# Correlation Analysis - Does one competitor affect others?
retscomp = dfcomp.pct_change()
corr = retscomp.corr()
print(corr)

# Plot GOOG and AIG with scatterPlot to view their return distribution
plt.scatter(retscomp.GOOG, retscomp.SPY)
plt.xlabel('Returns GOOG')
plt.ylabel('Returns SPY')
plt.legend()
plt.show()
"""
Conclusion: The scatter plot shows that during 2017-08-03 to 2020-08-03, there are
relatively strong positive correlations among GOOG returns and AIG returns. The 
higher the GOOG returns, the higher AIG returns as well for most cases.
"""