import math
import pandas as pd
import model.loaddata as load
import model.readdata as read
import matplotlib.pyplot as plt
import numpy as np


class RiskModel:

    def __init__(self, start_date, end_date, *args):
        load.get_data_by_tickets(start_date, end_date, *args)
        self.all_data = read.read_data(*args)

    def calcVaR(self, confidentLevel, *args):
        df = pd.DataFrame()
        price = []

        for key, itm in self.all_data.items():
            df[key] = (itm['Adj Close'] - itm['Adj Close'].shift(1)) / itm['Adj Close']
            price.append(itm['Adj Close'].iloc[-1])

        pos = np.array([arg for arg in args])
        pos = np.multiply(pos, np.array(price))
        pos = np.array(pos)
        # drop na
        df = df.iloc[1:]
        # convariance of the matrix
        cov = np.array(df.cov())
        # X'EX
        res = pos.dot(cov)
        res = res.dot(np.transpose(pos))
        # return the confident level VaR
        return -1 * confidentLevel * math.sqrt(res)


#   monte carlos simulation
    def monteCarlos(self, nums, confidentLevel, *args):
        df = pd.DataFrame()
        price = []

        for key, itm in self.all_data.items():
            df[key] = (itm['Adj Close'] - itm['Adj Close'].shift(1)) / itm['Adj Close']
            price.append(itm['Adj Close'].iloc[-1])

        meanVar = df.mean(axis=0)
        cov = df.cov()
        # Cholesky Decomposition
        cholesky = np.linalg.cholesky(cov)

        ret = pd.DataFrame(columns=[x for x in df.columns.values])
        for i in range(nums):
            randomVar = [np.random.normal() for _ in range(len(df.columns.values))]
            tmp = np.transpose(meanVar + np.transpose(randomVar).dot(cholesky))
            ret = ret.append(tmp, ignore_index=True)
        # calculate the monte carlos number by applying the current position
        pos = np.array([arg for arg in args])
        pos = np.multiply(pos, np.array(price))
        ret *= pos
        ret['combine'] = ret.sum(axis=1)
        ret = ret.sort_values(by=['combine'])
        # return the value with confidentlevel that user defined
        return ret['combine'].iloc[int(len(ret) * confidentLevel)]


if __name__ == '__main__':

    testObj = RiskModel('2018-1-1', '2018-12-31', 'AAPL', 'IBM')
    position = [100, 100]
    print(testObj.monteCarlos(100, 0.05, 100, 100))
    print(testObj.calcVaR(2.33, position))
    # a = pd.DataFrame(np.random.rand(2, 2))
    # cov = a.cov()
    # rand = np.random.rand(20000, 2)
    # # rand = np.random.normal(0, 1)
    #
    # engValue, engVector = np.linalg.eig(cov)
    # # engValue = np.linalg.eigvals(cov)
    # diagonal = np.diag(engValue)
    # diagonal = np.sqrt(diagonal)
    # res = diagonal.dot(np.transpose(engVector))
    # res = rand.dot(res)
    # # print(res)
    #
    # print(pd.DataFrame(res).cov())
    # print(cov)
