#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from multiprocessing import Pool
import model.StrategyModel as mvModel
import pandas as pd


class BackTester:

    # __slots__ = ('model', 'ticker', 'start', 'end', 'p_size', 'trade_lot')

    def __init__(self, ticker, start_date, end_date, p_size=1000, lot_size=1):
        self.mvModel = mvModel.MvTrade(ticker, start_date, end_date, p_size, lot_size)

    def add_model(self, start, end):

        ret = []
        for i in range(start, end):
            for j in range(i+1, end + 1):
                self.mvModel.fst_mv = i
                self.mvModel.slw_mv = j
                ret.append([i, j, self.mvModel.total_pnl()])
        # print(self.test_output.head())
        return ret

    def process_test(self, start, end):
        ret = pd.DataFrame(columns=['fst_mv', 'slw_mv', 'ttl_pnl'])
        cnt = (end - start) // 4
        all_task = [(i, i + cnt) for i in range(start, end, cnt)]
        results = Pool(4).starmap(self.add_model, all_task)

        for i in results:
            for j in i:
                # print(j)
                ret.loc[len(ret)] = j
        return ret


if __name__ == '__main__':

    test = BackTester('spy', '2018-1-1', '2018-12-31')
    test_ret = test.process_test(1, 20)
    print(test_ret)
    # df = test.add_model(testTrade)
    # print(df)
