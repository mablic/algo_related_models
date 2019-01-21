#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas_datareader as web
import os


def get_data_by_tickets(start_date, end_date, *tickers, source='yahoo'):
    for ticker in tickers:
        df = web.DataReader(ticker, source, start_date, end_date)
        df.to_csv(os.getcwd() + '\\%sdata.csv' % ticker)



