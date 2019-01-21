#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import os


def read_data(*tickers):
    all_data = {}
    for ticker in tickers:
        df = pd.read_csv(os.getcwd() + '\\%sdata.csv' %ticker, index_col=None)
        if ticker not in all_data.keys():
            all_data[ticker] = df
        else:
            raise "ticker %s already existed." % ticker
    return all_data
