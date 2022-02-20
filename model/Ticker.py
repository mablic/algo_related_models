#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import pandas
import os
from datetime import datetime, timedelta

class Ticker:

    def __init__(self, ticker) -> None:
        f = open(os.getcwd() + '/model/config/config.json')
        jsonData = json.load(f)
        self.configKey = jsonData['polygon_key']
        self.__name = ticker
        self.__data = None
        self.__startDate = '1990-01-01'
        self.__endDate = '1990-01-01'

    def import_data_range(self, startDate, endDate):
        format = "%Y-%m-%d"
        try:
            # data = requests.get('https://api.polygon.io/v2/aggs/ticker/' + self._name 
            #     + '/range/1/day/' + startDate + '/' + endDate + '?adjusted=true&sort=asc&limit=120&apiKey=' + self.configKey).json()
            datetime.strptime(startDate, format)
            datetime.strptime(endDate, format)
            format = "%Y-%m-%d"
            yrsDiff = (datetime.strptime(endDate, format) - datetime.strptime(startDate, format)).total_seconds() // 31536000
            if yrsDiff > 2:
                raise "Invalid data range, can't load data more than 2 years."
            f = open(os.getcwd() + '/model/data/AAPL.json')
            data = json.load(f)
            df = pandas.DataFrame(data['results'])
            df = df[['t','o','h','l','c','v','vw','n']]
            df.rename(columns={'t': 'Date','o': 'Open','h': 'High','l': 'Low','c': 'Close','v': 'Volume'}, inplace=True)
            df['Date'] = pandas.to_datetime(df['Date'], unit='ms')
            df.index = pandas.DatetimeIndex(df['Date'])
            self.__startDate = startDate
            self.__endDate = endDate
            self.__data = df
        except ValueError: 
            raise "time data 'time' does not match format '%Y-%m-%d"
        except:
            raise "Import data fail error!"

    def set_data_range(self, startDate, endDate):
        format = "%Y-%m-%d"
        if datetime.strptime(self.__startDate, format) > datetime.strptime(startDate, format) or datetime.strptime(self.__endDate, format) < datetime.strptime(endDate, format):
            self.import_data_range(startDate, endDate)
        else:
            mask = (self.__data['Date'] >= startDate) & (self.__data['Date'] <= datetime.strptime(endDate, format) + timedelta(1))
            self.__startDate = startDate
            self.__endDate = endDate
            self.__data = self.__data.loc[mask]

    def get_data(self):
        return self.__data

    def check_if_has_data(self):
        return self.__name != None

    def get_ticker_name(self):
        return self.__name

    def print_data_range(self):
        print(self.__data)

if __name__ == '__main__':

    t = Ticker('AAPL')
    t.import_data_range('2021-06-01','2021-06-30')
    t.print_data_range()
    t.set_data_range('2021-06-15', '2021-06-28')
    t.print_data_range()
