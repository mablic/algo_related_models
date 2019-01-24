import pandas as pd
import pandas_datareader as web
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os
from mpl_finance import candlestick_ohlc
from datetime import datetime as dt


def get_data(ticket, startdate, enddate, source='yahoo'):
	df=web.DataReader(ticket, source, startdate, enddate)
	df.to_csv(os.getcwd() + '\\%sdata.csv' % ticket)

def read_data(ticket):
	df = pd.read_csv(os.getcwd() + '\\%sdata.csv' %ticket, index_col=None)
	return df

def graph_data(df, mv1, mv2):
	df['Date'] = pd.datetools.to_datetime(df['Date'])
	df['Date'] = df['Date'].map(mdates.date2num)

	df_ohlc = df[mv2:]
	df_ohlc = df_ohlc[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
	df_ohlc[str(mv1) + 'ma'] = df['Close'].rolling(mv1).mean()
	df_ohlc[str(mv2) + 'ma'] = df['Close'].rolling(mv2).mean()

	fig = plt.figure()
	ax1 = plt.subplot2grid((6, 1), (0, 0), rowspan=5, colspan=1)
	ax2 = plt.subplot2grid((6, 1), (5, 0), rowspan=1, colspan=1, sharex=ax1)
	ax1.xaxis_date()
	candlestick_ohlc(ax1, df_ohlc.values, width=0.5, colorup='#77d879', colordown='#db3f3f')
	ax1.plot(df_ohlc.Date, df_ohlc[str(mv1) + 'ma'], color='b', label=str(mv1) + ' days moving average.')
	ax1.plot(df_ohlc.Date, df_ohlc[str(mv2) + 'ma'], color='r', label=str(mv2) + ' days moving average.')
	ax2.bar(df_ohlc.Date, df_ohlc.Volume)
	plt.setp(ax1.get_xticklabels(), visible=False)

	ax1.set_title('%d days moving average vs %d days moving average.' % (mv1, mv2) )
	ax1.legend(loc='best')
	for label in ax2.xaxis.get_ticklabels():
		label.set_rotation(45)

	plt.show()

if __name__ == '__main__':
	#get_data('spy', '2017-1-1', '2018-11-30')

	df = read_data('spy')
	graph_data(df, 10, 20)
