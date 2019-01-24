#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas_datareader as web
import os


def get_data_by_tickets(start_date, end_date, *tickers, source='yahoo'):
    for ticker in tickers:
        try:
            df = web.DataReader(ticker, source, start_date, end_date)
            df.to_csv(os.getcwd() + '\\data\\%sdata.csv' % ticker)
        except ValueError:
            print("Ticker %s is not valid." % ticker)



