import pandas as pd
import model.loaddata as load
import model.readdata as read
import matplotlib.pyplot as plt


class MvTrade:

    def __init__(self, ticker, start_date, end_date, fst_mv, slw_mv, p_size=1000, trade_lot=1):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.fst_mv = fst_mv
        self.slw_mv = slw_mv
        self.p_size = p_size
        self.trade_lot = trade_lot
        try:
            load.get_data_by_tickets(self.start_date, self.end_date, self.ticker)
        except ValueError:
            raise "Load data error for ticker %s." % self.ticker

    def mv_position(self):
        try:
            df = read.read_data(self.ticker)[self.ticker]
        except ValueError:
            raise "No data for ticker %s." % self.ticker

        # calc moving average
        df['fst_mv'] = df['Close'].rolling(self.fst_mv).mean()
        df['slw_mv'] = df['Close'].rolling(self.slw_mv).mean()
        df['diff'] = df['fst_mv'] - df['slw_mv']
        df['signal_today'] = df['diff'].apply(lambda x: -1 if x <= 0 else 1)
        return df[['Date', 'Close', 'signal_today']]

    def pnl(self):
        runningPnL = []
        pos = self.mv_position()
        entry_pos = 0
        for i in range(len(pos['signal_today'])):
            if i == 0:
                runningPnL.append(0)
            elif i > 0 and pos['signal_today'][i] != pos['signal_today'][i-1]:
                self.calc_pnl(runningPnL, entry_pos,
                              pos['Close'][i-1] * self.trade_lot, pos['Close'][i] * self.trade_lot)
                entry_pos = pos['signal_today'][i]
            else:
                self.calc_pnl(runningPnL, entry_pos,
                              pos['Close'][i-1] * self.trade_lot, pos['Close'][i] * self.trade_lot)
            if sum(runningPnL) + self.p_size <= 0:
                # broke
                break
        running_pnl = pd.DataFrame(runningPnL, index=pos.Date, columns=['running_pnl'])
        # running pnl is the running pnl dataframe with date as index
        return running_pnl

    def calc_pnl(self, runningPnL, entry_pos, prev_price, cur_price):
        # calculate pnl by using position between yesterday and today
        if entry_pos == 0:
            runningPnL.append(0)
        elif entry_pos > 0:
            # for long position
            runningPnL.append(cur_price - prev_price)
        else:
            # for short position
            runningPnL.append(prev_price - cur_price)

    def total_pnl(self):
        return sum(self.pnl()['running_pnl'])

    def total_capital(self):
        return sum(self.pnl()['running_pnl']) + self.p_size

    def graph_pnl(self, agg='M'):
        # communicate pnl with line graph
        # running pnl with bar graph
        # graph aggregate by month

        df = self.pnl()
        df['cum_pnl'] = df['running_pnl'] + df['running_pnl'].shift()
        df.index = pd.to_datetime(df.index)

        df = df.groupby(pd.Grouper(freq=agg)).agg('sum')

        ax1 = plt.subplot2grid((8, 1), (0, 0), rowspan=5, colspan=1)
        ax2 = plt.subplot2grid((8, 1), (5, 0), rowspan=3, colspan=1, sharex=ax1)

        ax1.plot(df.index, df.cum_pnl)
        ax2.bar(df.index, df.running_pnl, width=30)

        ax1.set_title('%s cummulative PnL and running PnL' % self.ticker)
        ax1.xaxis.set_visible(False)
        ax1.legend(loc='best')

        for label in ax2.xaxis.get_ticklabels():
            label.set_rotation(45)

        ax1.set_ylabel('PnL')
        # plt.xlabel('Date')
        plt.show()


if __name__ == '__main__':
    testTrade = MvTrade('spy', '2018-1-1', '2018-12-31', 10, 20, 1000, 1)
    testTrade.graph_pnl()
    # print(testTrade.pnl())
    # print("Total Capital is : %.2f." % testTrade.total_capital())
