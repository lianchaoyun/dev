from __future__ import (absolute_import, division, print_function, unicode_literals)
from datetime import datetime
import backtrader as bt
import pandas as pd
import tushare as ts
from backtrader.feeds import PandasData
from mootdx.reader import Reader
from mootdx.quotes import Quotes

reader = Reader.factory(market='std', tdxdir='C:/app/海皇星')
env = 1
if env == 1:
    client = Quotes.factory(market='std', multithread=True, heartbeat=True)
    df = client.bars(symbol='601658', adjust='qfq', frequency=9, offset=235)
    df.dropna(axis=0, subset=["open"], inplace=True)
    df.drop("factor", axis=1, inplace=True)
    df.drop("datetime", axis=1, inplace=True)
    df.drop("year", axis=1, inplace=True)
    df.drop("month", axis=1, inplace=True)
    df.drop("day", axis=1, inplace=True)
    df.drop("hour", axis=1, inplace=True)
    df.drop("minute", axis=1, inplace=True)
    df.drop("vol", axis=1, inplace=True)
    # df = reader.daily(symbol='600036')
    # df['ma10'] = talib.MA(df['close'], timeperiod=10, matype=0)
    #df.columns = ["date"] + df.columns[1:].tolist()
    #df.set_index("date")
    df.to_csv("s1.csv", float_format='%.2f')
    df.index.name="date"
else:
    df = pd.read_csv("s1.csv", index_col=0, parse_dates=True)


class TestFixedSize(bt.Sizer):
    def _getsizing(self, comminfo, cash, data, isbuy):
        position = self.broker.getposition(data)
        size = self.p.stake * (1 + (position.size != 0))
        return size


# Create a Stratey
class TestStrategy(bt.Strategy):

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.sma = bt.indicators.SimpleMovingAverage(self.datas[0].close, period=20)
        self.last_price = 0

    def notify_trade(self, trade):
        pass

    def notify_order(self, order):
        pass

    def fmt_pd(self, pd, dif_rate="-"):
        pdd = pd[0]
        print(pdd.datetime.date(0), "\t",
              #pdd.open[0], "\t",
              #pdd.high[0], "\t",
              #pdd.low[0], "\t",
              "%.2f" %pdd.close[0], "\t",
             # pdd.volume[0], "\t",
              "%.f" % cerebro.broker.getvalue(), "\t",
              self.position.size, "\t",
              "%.3f" % dif_rate, "\t",
              )

    def next(self):
        close = self.datas[0].close[0]
        dif_rate = (close - self.last_price) / close
        buy_money = close * 1000
        if self.last_price == 0:
            self.buy(size=10000)
            self.last_price = close
            self.fmt_pd(self.datas,dif_rate)
            return

        if dif_rate < -0.017 and cerebro.broker.getcash() > buy_money:
            self.buy(size=1000)
            self.last_price = close
            self.fmt_pd(self.datas,dif_rate)
            return

        if dif_rate >= 0.017 and self.position.size >= 100:
            self.sell(size=1000)
            self.last_price = close
            self.fmt_pd(self.datas,dif_rate)
            return


if __name__ == '__main__':
    cerebro = bt.Cerebro()

    cerebro.broker.setcash(200000)

    cerebro.addsizer(bt.sizers.FixedSize, stake=100)

    cerebro.broker.setcommission(commission=0.0001)

    cerebro.addstrategy(TestStrategy)

    cerebro.adddata(bt.feeds.PandasData(dataname=df,
                                        fromdate=df.index[0],
                                        todate=df.index[-1],
                                        #fromdate=datetime(2020, 9, 23),
                                        #todate=datetime(2024, 1, 10)
                                        ))

    cerebro.run()

    print('资产: %.2f' % cerebro.broker.getvalue())
    print("现金: %.2f" % cerebro.broker.getcash())

cerebro.plot()
