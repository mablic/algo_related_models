#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from matplotlib import ticker
import pandas as pd
import mplfinance as mpf
from datetime import datetime
from Ticker import Ticker


class PlotType:
    candle = 'candle'
    line = 'line'
    renko = 'renko'
    pnf = 'pnf'
    ohlc = 'ohlc'

class GraphData:
    
    def __init__(self) -> None:
        self.__ticker = None
        self.__startDate = '1990-01-01'
        self.__endDate = '1990-01-01'

    def set_data(self, ticker, start, end, type='line'):
        format = "%Y-%m-%d"
        try:
            self.__ticker = ticker
            datetime.strptime(start, format)
            datetime.strptime(end, format)
            self.__startDate = start
            self.__endDate = end
            self.__type = type
        except ValueError:
            raise print("Invalid input for the datetime. It should be YYYY-MM-DD")

    def get_plot_base(self):
        return self.__ticker, self.__type

    def graph_plot(self):
        if not self.__ticker.check_if_has_data():
            self.__ticker.import_data_range(self.__startDate, self.__endDate)
        else:
            self.__ticker.set_data_range(self.__startDate, self.__endDate)
        mpf.plot(self.__ticker.get_data(), type=self.__type, volume=True)

class DecoratorGraph(GraphData):

    def __init__(self, graphData) -> None:
        super().__init__()
        self._graphData = graphData
        self._ticker, self._type = graphData.get_plot_base()
    
class DecoratorMV(DecoratorGraph):
    
    def set_plot(self, graphData) -> None:
        super().__init__(graphData)
        self.__mv = []

    def add_mv(self, mv):
        self.__mv.append(mv)

    def graph_plot(self):
        mpf.plot(self._ticker.get_data(), type=self._type, mav=tuple(self.__mv), volume=True)

if __name__ == '__main__':

    t = Ticker('AAPL')
    t.import_data_range('2021-06-01','2021-06-30')
    t.print_data_range()

    g = GraphData()
    g.set_data(t, '2021-06-15','2021-06-30')
    # g.graph_plot()

    mv = DecoratorMV(g)
    mv.set_plot(g)
    mv.add_mv(3)
    mv.add_mv(5)
    mv.graph_plot()
