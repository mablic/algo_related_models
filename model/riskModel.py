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
        return confidentLevel * math.sqrt(res)


#   still in process.
#     def monteCarlos(self):
#         df = pd.DataFrame()
#         price = []
#
#         for key, itm in self.all_data.items():
#             df[key] = (itm['Adj Close'] - itm['Adj Close'].shift(1)) / itm['Adj Close']
#             price.append(itm['Adj Close'].iloc[-1])
#
#         #covariance
#         cov = df.cov()
#         #engValue & engVector
#         engValue, engVector = np.linalg.eig(cov)
#         #sqrt root of the diagonal engValue
#         diagonal = np.sqrt(np.diag(engValue))
#         res = diagonal.dot(np.transpose(engVector))
#         randInt = np.random.rand(1000, 2)
#         res = randInt.dot(res)
#         res = pd.DataFrame(res)
#
#         return res.cov(), cov


if __name__ == '__main__':

    testObj = RiskModel('2018-1-1', '2018-12-31', 'AAPL', 'IBM')
    print(testObj.monteCarlos())
    # position = [100, 100]
    # print(testObj.calcVaR(2.33, position))
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
