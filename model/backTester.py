import model.mvTradeModel as mvModel
import pandas as pd

class BackTester:

    # __slots__ = ('model', 'ticker', 'start', 'end', 'p_size', 'trade_lot')

    def __init__(self, start, end):
        self.start = start
        self.end = end

    def add_model(self, model):
        try:
            isinstance(model, mvModel.MvTrade)
        except TypeError:
            print("Model is not valid.")

        ret = pd.DataFrame(columns=['fst_mv', 'slw_mv', 'pnl'])
        for i in range(self.start, self.end):
            for j in range(i+1, self.end + 1):
                model.fst_mv = i
                model.slw_mv = j
                ret = ret.append({'fst_mv': i, 'slw_mv': j, 'pnl': model.total_pnl()}, ignore_index=True)

        return ret


if __name__ == '__main__':

    testTrade = mvModel.MvTrade('spy', '2018-1-1', '2018-12-31', 1000, 1)
    testTrade.fst_mv = 10
    testTrade.slw_mv = 20

    test = BackTester(5, 10)
    df = test.add_model(testTrade)
    print(df)
