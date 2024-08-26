from datetime import datetime
from mootdx.reader import Reader
from mootdx.quotes import Quotes
import pandas as pd
import numpy as np
from datetime import date
pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)
reader = Reader.factory(market='std', tdxdir='C:/app/海皇星')

cash = 0  #现金
position = 0 #持仓
last_price = 0 #上次开仓价格

def dataTest(env,symbol,period):
    if env == 1:
        client = Quotes.factory(market='std', multithread=True, heartbeat=True)
        df = client.bars(symbol='301263', adjust='qfq', frequency=9,
                         offset=800)  # frequency -> K线种类 0 => 5分钟K线 => 5m 1 => 15分钟K线 => 15m 2 => 30分钟K线 => 30m 3 => 小时K线 => 1h 4 => 日K线 (小数点x100) => days 5 => 周K线 => week 6 => 月K线 => mon 7 => 1分钟K线(好像一样) => 1m 8 => 1分钟K线(好像一样) => 1m 9 => 日K线 => day 10 => 季K线 => 3mon 11 => 年K线 => year
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
        # df.columns = ["date"] + df.columns[1:].tolist()
        # df.set_index("date")
        df.index.name = "date"
        df.to_csv("s1.csv", float_format='%.2f')
    elif env == 2:
        import akshare as ak
        dfsina = ak.futures_zh_minute_sina(symbol=symbol, period=period)
        dfsina.dropna(axis=0, subset=["open"], inplace=True)
        dfsina = dfsina.rename(columns={'hold': 'amount'})
        dfsina = dfsina.rename(columns={'datetime': 'date'})
        dfsina['date'] = pd.to_datetime(dfsina['date'])
        # dfsina.index.name = "date"
        dfsina.set_index('date', inplace=True)
        df = dfsina
        #df.to_csv("s2.csv", float_format='%.2f')
    else:
        df = pd.read_csv("s1.csv", index_col=0, parse_dates=True)
    # print(df)
    return df

df = dataTest(2,"SA2409",60)

df["ma20"] = df["close"].rolling(window=30).mean()

def apply_test(row):
    is_last = row.equals(df.iloc[-1])
    global position, cash, last_price
    close = row["close"]
    ma20 = row["ma20"]
    dif_ma = close - ma20
    pin = False
    tmp_price = 0
    if close > ma20:
        if position < 0:  # 平空
            dif_price = last_price - close
            cash += dif_price
            position = 0
            pin = True
            tmp_price = dif_price
        if position == 0:  # 开多
            last_price = close
            position = 1
    if close < ma20:
        if position > 0:  # 平多
            dif_price = close - last_price
            cash += dif_price
            position = 0
            pin = True
            tmp_price = dif_price
        if position == 0:  # 开空
            last_price = close
            position = -1
    if is_last and position != 0:
        if position < 0:  # 平空
            dif_price = last_price - close
            cash += dif_price
            position = 0
            pin = True
            tmp_price = dif_price
        if position > 0:  # 平多
            dif_price = close - last_price
            cash += dif_price
            position = 0
            pin = True
            tmp_price = dif_price
    if pin:
        return [round(dif_ma, 2), "", round(tmp_price, 2), "", position, "", round(cash, 2)]
    else:
        return "-"

df["rs"] = df.apply(apply_test, axis=1)
print(df.reset_index()[['date', 'close', "rs"]])
print("\n",df.iloc[-1])


