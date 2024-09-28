'''
from ctpbee import CtpBee
from ctpbee import CtpbeeApi
from ctpbee.constant import *
from ctpbee import hickey
import datetime
from datetime import date
import time
import math
from tqsdk import TqApi, TqAuth, TqKq, TqAccount, TqBacktest
from cm import fmt_float, ts2time, symbol_short_name, ts2timestamp, fmt_futures
from threading import Thread
from time import sleep
from lib.eventbus import eventbus, subscriber, event


class CTATQ():
    def __init__(self, env, api, instrument_set, open_long=1, open_short=1, trade_timeout=600,minutek=15):
        self.env = env
        self.api = api
        self.order = None
        self.strategy = "KT"
        self.instrument_set = instrument_set
        self.open_long = open_long
        self.open_short = open_short
        self.trade_timeout = trade_timeout
        self.minutek = minutek
        self.isRun = True
        self.inittq()

    def inittq(self):
        try:
            self.quote = self.api.get_quote(self.instrument_set[0])
            self.klines = self.api.get_kline_serial(self.instrument_set[0], self.minutek * 60)
            self.position = self.api.get_position(self.instrument_set[0])
            self.orders = self.api.get_order()
        except Exception as ex:
            print("\n tq init _ {0} _ \n{1!r}".format(type(ex).__name__, ex.args))
            self.isRun = False
            if self.api: self.api.close()

    def get_order_symbol(self, order):
        return order[1].exchange_id + "." + order[1].instrument_id

    def get_trade_lasttime(self):
        trades = self.api.get_trade()
        tmptime = 0
        for td in trades.items():
            symbol = self.get_order_symbol(td)
            if symbol == self.instrument_set[0]:
                if td[1].trade_date_time > tmptime:
                    tmptime = td[1].trade_date_time
        return ts2timestamp(tmptime)

    def on_quote(self, qtime, instrument, last_price, dif_c_ma, dif_p_av):
        is_long = dif_c_ma > 0 and dif_p_av > 0
        is_short = dif_c_ma < 0 and dif_p_av < 0
        lasttime = self.get_trade_lasttime()
        # 挂单处理
        orders_alive = dict(
            filter(lambda od: od[1].status == "ALIVE" and instrument == self.get_order_symbol(od),
                   self.orders.items()))
        print(ts2time(qtime), symbol_short_name(instrument), last_price, dif_c_ma, dif_p_av, "(",
              self.position.pos_long, self.position.pos_short, ")", len(orders_alive), ts2time(lasttime))
        for od in orders_alive.items():
            timeout = time.time() - ts2timestamp(od[1].insert_date_time)
            if timeout > 180:  # 3分钟不成交则取消
                self.api.cancel_order(od[0])
                fmt_futures(ts=ts2time(time.time()), strategy=self.strategy, symbol=self.instrument_set[0],
                            op="撤单:" + od[0])
                if self.env != 3: sleep(18)
                self.api.wait_update(deadline=time.time() + 10)
                return

        if self.env != 3 and len(orders_alive) > 0:
            return

        if self.env != 3 and self.order:
            od = self.api.get_order(self.order['order_id'])
            if od and od.status == "ALIVE":
                return
            else:
                self.order = None

        # 平仓处理
        if is_long and (self.position.pos_short_his > 0 or self.position.pos_short_today > 0):
            print("平空单")
            self.order = self.api.insert_order(symbol=self.instrument_set[0], direction="BUY",
                                               offset="CLOSE" if self.position.pos_short_his > 0 else "CLOSETODAY",
                                               limit_price=last_price,
                                               volume=self.position.pos_short_his if self.position.pos_short_his > 0 else self.position.pos_short_today)
            if self.env != 3: sleep(18)
            if self.env != 3: self.api.wait_update(deadline=time.time() + 18)
            return
        elif is_short and (self.position.pos_long_his > 0 or self.position.pos_long_today > 0):
            print("平多单")
            self.order = self.api.insert_order(symbol=self.instrument_set[0], direction="SELL",
                                               offset="CLOSE" if self.position.pos_long_his > 0 else "CLOSETODAY",
                                               limit_price=last_price,
                                               volume=self.position.pos_long_his if self.position.pos_long_his > 0 else self.position.pos_long_today)

            if self.env != 3: self.api.wait_update(deadline=time.time() + 18)
            if self.env != 3: sleep(18)
            return

        if self.env != 3 and time.time() - lasttime < self.trade_timeout:
            # print("上次成交时间:",ts2time(lasttime))
            return

        pos = self.position.pos_long_his + self.position.pos_long_today + self.position.pos_short_his + self.position.pos_short_today
        # 开仓处理
        if self.open_long > 0 and is_long and pos < 1:
            print("开多单")
            self.order = self.api.insert_order(symbol=self.instrument_set[0], direction="BUY", offset="OPEN",
                                               limit_price=last_price,
                                               volume=self.open_long)
            if self.env != 3: self.api.wait_update(deadline=time.time() + 18)
            if self.env != 3: sleep(18)
        elif self.open_short > 0 and is_short and pos < 1:
            print("开空单")
            self.order = self.api.insert_order(symbol=self.instrument_set[0], direction="SELL", offset="OPEN",
                                               limit_price=last_price,
                                               volume=self.open_short)
            if self.env != 3: self.api.wait_update(deadline=time.time() + 18)
            if self.env != 3: sleep(18)

    def run(self):
        try:
            if self.api is None: return
            if self.api.is_changing(self.quote) or self.api.is_changing(self.klines):
                ma = sum(self.klines.close.iloc[-20:]) / 20
                if self.env == 3:
                    if self.quote.last_price > ma:
                        self.quote.average = self.quote.last_price + 1
                    elif self.quote.last_price < ma:
                        self.quote.average = self.quote.last_price - 1
                    else:
                        self.quote.average = 0
                if math.isnan(ma) or math.isnan(self.quote.last_price) or math.isnan(self.quote.average): return
                dif_c_ma = fmt_float(self.klines.close.iloc[-1] - ma)
                dif_p_av = fmt_float(self.quote.last_price - self.quote.average)
                self.on_quote(self.quote.datetime, self.instrument_set[0], self.quote.last_price, dif_c_ma, dif_p_av)

        except Exception as ex:
            print("\n tq run  _ {0} _ \n{1!r}".format(type(ex).__name__, ex.args))
            self.isRun = False
            if self.api: self.api.close()


def start():
    env = 2
    strategy_list = []
    if env == 1:
        api = TqApi(TqAccount("H徽商期货", "807599", "meng12051206"),
                    # auth=TqAuth("meng423522", "meng423522"),
                    auth=TqAuth("wuzhenzhen", "meng423522"),
                    web_gui="http://0.0.0.0:9876")
    elif env == 2:
        api = TqApi(TqKq(),
                    auth=TqAuth("meng423522", "meng423522"),
                    # auth=TqAuth("wuzhenzhen", "meng423522"),
                    web_gui="http://0.0.0.0:9876")
    else:
        start_date = date(2023, 11, 1)
        end_date = datetime.date.today()
        api = TqApi(
            backtest=TqBacktest(start_dt=start_date, end_dt=end_date),
            # auth=TqAuth("meng423522", "meng423522"),
            auth=TqAuth("wuzhenzhen", "meng423522"),
            web_gui="http://0.0.0.0:9876")

    #strategy_list.append(CTATQ(env=env, api=api, instrument_set=['SHFE.ag2403'], open_long=1, open_short=1, trade_timeout=600))
    strategy_list.append(CTATQ(env=env, api=api, instrument_set=['DCE.a2403'], open_long=1, open_short=1, trade_timeout=600))
    strategy_list.append(CTATQ(env=env, api=api, instrument_set=['DCE.m2405'], open_long=1, open_short=0, trade_timeout=1200))
    strategy_list.append(CTATQ(env=env, api=api, instrument_set=['CZCE.RM411'], open_long=1, open_short=0, trade_timeout=3000,minutek=60))
    strategy_list.append(CTATQ(env=env, api=api, instrument_set=['SHFE.fu2403'], open_long=1, open_short=0, trade_timeout=900))

    while True:
        flag = False
        api.wait_update(deadline=time.time() + 10)
        for stra in strategy_list:
            if stra is None or not stra.isRun:
                flag = True
                break
            stra.run()
        if flag:
            break
        if env != 3: time.sleep(2)


if __name__ == '__main__':
    start()
#pkill -f tq.py && cd /www/wwwroot/loli &&  rm -rf nohup.out && nohup python  tq.py &

'''
from datetime import date
from datetime import datetime

def tqTest():
    from tqsdk import TqApi, TqAuth, TqKq, TqAccount, TqBacktest
    envapi = 2
    if envapi == 1:  # 实盘
        api = TqApi(TqAccount("H徽商期货", "807599", "meng12051206"),
                    # auth=TqAuth("meng423522", "meng423522"),
                    auth=TqAuth("wuzhenzhen", "meng423522"),
                    web_gui="http://0.0.0.0:9876")
    elif envapi == 2:  # 模拟
        api = TqApi(TqKq(),
                    auth=TqAuth("meng423522", "meng423522"),
                    # auth=TqAuth("wuzhenzhen", "meng423522"),
                    web_gui="http://0.0.0.0:9876")
    else:  # 回测
        start_date = date(2023, 11, 1)
        end_date = datetime.date.today()
        api = TqApi(
            backtest=TqBacktest(start_dt=start_date, end_dt=end_date),
            # auth=TqAuth("meng423522", "meng423522"),
            auth=TqAuth("wuzhenzhen", "meng423522"),
            web_gui="http://0.0.0.0:9876")

    klines = api.get_kline_serial("SHFE.ni2409", 15)
    print(klines)
    while True:
        api.wait_update()
        print("最后一根K线收盘价", klines.close.iloc[-1])


#print(df["close"].sum()/len(df))
#def apply_test(x):
#    return x**2
#print(df["close"].apply(apply_test))
#print(df*2)
#print(df["close"].agg(['min', 'max', 'std']))
#print(df.groupby("close"))

# for index, row in df.iterrows():
#    print(index,"  ",row)
#df2 = df.index.to_frame(name='date')


def test():
    tqTest()
    pass


if __name__ == '__main__':
    test()
    pass