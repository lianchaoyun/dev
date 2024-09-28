# coding=utf-8
from __future__ import print_function, absolute_import
import pandas as pd
import pandas_ta as ta
import time
from gm.api import *
import talib
import os
from threading import Thread
from time import sleep


def ts2time(ts):
    if isinstance(ts, str):
        if len(ts) > 19:
            ts = ts[0:19]
        return time.strftime("%Y-%m-%d %H:%M:%S", time.strptime(ts, "%Y-%m-%d %H:%M:%S"))

    if len(str(ts)) < 10:
        return "0000-00-00 00:00:00"
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(str(int(ts))[0:10])))


fmt_counter1 = 0


def symbol2market(all_stocks, sec_id):
    s = all_stocks.query('sec_id == ["' + sec_id + '"]')
    # print(s['symbol'].values[0])
    return s


# 策略中必须有init方法
def init(context):

    context.symbol1 = "SHFE.ag2410"
    context.strategy = 1
    context.frequency1 = "3600s"  # 3600s 7200s 1d
    context.long = 20
    context.all_stocks = get_instruments(exchanges='SZSE,SHSE', sec_types=1, df=1)
    #print(context.all_stocks)
    context.stock = symbol2market(context.all_stocks, context.symbol1)
    #context.symbol1 = context.stock['symbol'].values[0]

    print("股票代码:", context.symbol1)
    subscribe(symbols=context.symbol1, frequency=context.frequency1, count=context.long)
    #subscribe(symbols=context.symbol1, frequency='tick')

def on_tick(context, tick):
    print(tick)
    print("均价:",tick.cum_amount/tick.cum_volume,tick.created_at)


def fmt_stock(ts, strategy, symbol, last_price, dif_average, dif_ma, dif_order, long, short):
    global fmt_counter1
    symbol = symbol.split(".")[1] if (symbol and "." in symbol) else symbol
    long = "多" if long != 0 else "-"
    short = "空" if short != 0 else "-"
    fmt = "{:10}\t{:^10}\t{:^5}\t{:^10}\t{:^5}\t{:5}\t{:^5}\t{:^5}\t{:^5}"
    if fmt_counter1 % 10 == 0:
        print_msg = fmt.format("时间", "策略", "代码", "最新", "均价", "昨收", "订单", "+", "-")
        print(print_msg)
    fmt_counter1 += 1
    print_msg = fmt.format(ts, strategy, symbol, last_price, dif_average, dif_ma, dif_order, long, short)
    print(print_msg)


def on_bar(context, bar):
    print(11)
    #sleep(5)
    # 打印当前获取的bar信息
    kdata = context.data(symbol=context.symbol1, frequency=context.frequency1, count=context.long)
    ma = talib.MA(kdata['close'].values, context.long)
    close1 = bar[0].close
    ma1 = ma[-1]
    dif_ma = close1 - ma1
    close1 = float('{:.2f}'.format(close1))
    dif_ma = float('{:.2f}'.format(dif_ma))
    if dif_ma > 0:
        vol = int(context.account().cash['available']/(close1*100))*100
        if vol < 1:
            return
        fmt_stock(ts=ts2time(time.time()),
                  strategy="均线",
                  symbol=context.symbol1,
                  last_price=close1,
                  dif_average="-",
                  dif_ma=dif_ma,
                  dif_order=vol,
                  long=True,
                  short=False,
                  )
        order_volume(symbol=context.symbol1, volume=vol, side=OrderSide_Buy,
                     position_effect=PositionEffect_Open, order_type=OrderType_Market)
    elif dif_ma < 0:
        position_long = context.account().position(symbol=context.symbol1, side=1)
        if position_long:
            vol = position_long['available']
            if vol < 1:
                return
            fmt_stock(ts=ts2time(time.time()),
                      strategy="均线",
                      symbol=context.symbol1,
                      last_price=close1,
                      dif_average="-",
                      dif_ma=dif_ma,
                      dif_order=vol,
                      long=False,
                      short=True,
                      )
            order_volume(symbol=context.symbol1, volume=vol, side=OrderSide_Sell,
                         position_effect=PositionEffect_Close,
                         order_type=OrderType_Market)


def on_backtest_finished(context, indicator):
    print("回测结果", indicator.pnl_ratio)


if __name__ == '__main__':
    '''
        strategy_id策略ID, 由系统生成
        filename文件名, 请与本文件名保持一致
        mode运行模式, 实时模式:MODE_LIVE回测模式:MODE_BACKTEST
        token绑定计算机的ID, 可在系统设置-密钥管理中生成
        backtest_start_time回测开始时间
        backtest_end_time回测结束时间
        backtest_adjust股票复权方式, 不复权:ADJUST_NONE前复权:ADJUST_PREV后复权:ADJUST_POST
        backtest_initial_cash回测初始资金
        backtest_commission_ratio回测佣金比例
        backtest_slippage_ratio回测滑点比例
        '''
    run(strategy_id='1492346a-5d5b-11ef-b2e2-a65e60bd3cfb',
        filename='Juejin.py',
        mode=MODE_BACKTEST,
        token='b9d7079e67207a8bb402206e72332c9ac2dd8165',
        backtest_start_time='2024-05-01 08:00:00',
        backtest_end_time='2024-08-12 16:00:00',
        backtest_adjust=ADJUST_PREV,
        backtest_initial_cash=100000,
        backtest_commission_ratio=0.0001,
        backtest_slippage_ratio=0.0001)

    print("*********main start***********")
    while True:
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        sleep(120)
    print("*********main end***********")
