#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import os
import json
from Ticker import Ticker
from bs4 import BeautifulSoup


class Data():

    def __init__(self) -> None:
        self.__tickerDict = {}
        f = open(os.getcwd() + '/model/config/config.json')
        jsonData = json.load(f)
        self.wikiPath = jsonData['wiki_path']
    
    def read_wiki(self):

        try:
            r = requests.get(self.wikiPath).text
            soup = BeautifulSoup(r)
            s = soup.find('table').find_all('a', {'external text'})

            for i in range(len(s)):
                if len(self.__tickerDict) > 500:
                    break
                if s[i].contents != ['reports']:
                    ticker = s[i].contents[0]
                    t = Ticker(ticker)
                    self.__tickerDict[ticker] = t
        except:
            raise "read wiki error!"

    def get_all_ticker(self):
        for i in self.__tickerDict.keys():
            print('Current Ticker is: %s' % self.__tickerDict[i].get_ticker_name())

    def check_if_ticker_exists(self, ticker):
        return ticker in self.__tickerDict

if __name__ == '__main__':
    d = Data()
    d.read_wiki()
    d.get_all_ticker()
