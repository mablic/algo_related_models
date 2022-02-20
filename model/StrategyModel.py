import pandas
import numpy
from Ticker import Ticker

class BaseStrategy:

    def __init__(self, ticker, start, end) -> None:
        self._ticker = ticker
        self._startDate = start
        self._endDate = end

class MovingAverageStrategy(BaseStrategy):

    def add_mv_line(self, mv1, mv2):
        df = self._ticker.get_data()
        df = df['Close'].to_frame()
        df['SMA' + str(mv1)] = df['Close'].rolling(mv1).mean()
        df['SMA' + str(mv2)] = df['Close'].rolling(mv2).mean()
        df = df.iloc[max(mv1, mv2): , :]
        df['Diff'] = (df['SMA' + str(mv1)] - df['SMA' + str(mv2)]) / abs(df['SMA' + str(mv1)] - df['SMA' + str(mv2)]) 
        df['Trade'] = numpy.sign(df['Diff']).diff().ne(0)
        print(df)

if __name__ == '__main__':
    t = Ticker('AAPL')
    t.import_data_range('2021-01-01','2021-12-31')
    t.print_data_range()

    mv = MovingAverageStrategy(t, '2021-06-01','2021-06-30')
    mv.add_mv_line(10, 20)