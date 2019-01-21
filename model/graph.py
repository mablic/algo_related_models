#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import model.readdata as read
from mpl_finance import candlestick_ohlc


COLOR = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']


def graph_data(ticker, *mvs):
    try:
        df_ohlc = read.read_data(ticker)[ticker]
    except ValueError:
        print('No csv file for ticker %s.' % ticker)

    max_date = max(mvs)
    df_ohlc['Date'] = pd.to_datetime(df_ohlc['Date'])
    df_ohlc['Date'] = df_ohlc['Date'].map(mdates.date2num)

    df_ohlc = df_ohlc[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
    for mv in mvs:
        df_ohlc[str(mv) + 'ma'] = df_ohlc['Close'].rolling(mv).mean()

    df_ohlc.drop([i for i in range(max_date)], inplace=True)
    fig = plt.figure()
    ax1 = plt.subplot2grid((6, 1), (0, 0), rowspan=5, colspan=1)
    ax2 = plt.subplot2grid((6, 1), (5, 0), rowspan=1, colspan=1, sharex=ax1)
    ax1.xaxis_date()
    candlestick_ohlc(ax1, df_ohlc.values, width=0.5, colorup='#77d879', colordown='#db3f3f')

    for i in range(len(mvs)):
        temp_color = COLOR[i % len(COLOR)]
        ax1.plot(df_ohlc.Date, df_ohlc[str(mvs[i]) + 'ma'], color=temp_color, label=str(mvs[i]) + ' days moving average.')
    #ax1.plot(df_ohlc.Date, df_ohlc[str(mv2) + 'ma'], color='r', label=str(mv2) + ' days moving average.')
    ax2.bar(df_ohlc.Date, df_ohlc.Volume)
    plt.setp(ax1.get_xticklabels(), visible=False)

    ax1.set_title('%s historical stock prices' % ticker)
    ax1.xaxis.set_visible(False)
    ax1.legend(loc='best')
    for label in ax2.xaxis.get_ticklabels():
        label.set_rotation(45)

    plt.show()


if __name__ == '__main__':
    #get_data('spy', '2017-1-1', '2018-11-30')
    graph_data('spy', 10, 20, 100)
