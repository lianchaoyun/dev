from hikyuu.interactive import *
from hikyuu import *
from datetime import datetime
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

# DataDriverFactory.regKDataDriver(PytdxKDataDriver())

sm.add_temp_csv_stock(code="RB2501",
                      day_filename="C:/project\hikyuu/test_data/test_day_data.csv",
                      min_filename="C:/project/hikyuu/test_data/test_min_data.csv"

                      )

print(sm["tmpRB2501"])
k = sm['tmpRB2501'].get_kdata(Query(-150))
print(k)

class DEMO_MM(MoneyManagerBase):
    def __init__(self):
        super(DEMO_MM, self).__init__("DEMO_MM")

    def _reset(self):
        pass

    def _clone(self):
        mm = DEMO_MM()
        return DEMO_MM()

    def _get_buy_num(self, datetime, stk, price, risk, part_from):
        tm = self.tm
        cash = tm.current_cash
        print("_get_buy_num", cash)
        return int(1000)

    def _get_sell_num(self, datetime, stk, price, risk, part_from):
        tm = self.tm
        position = tm.get_position(datetime, stk)
        current_num = int(position.number * 0.5)
        print("_get_sell_num", current_num)
        return current_num  # 返回类型必须是整数


def TurtleSG(self, k):
    n1 = self.get_param("n1")
    n2 = self.get_param("n2")
    c = CLOSE(k)
    h = REF(HHV(c, n1), 1)  # 前n日高点
    L = REF(LLV(c, n2), 1)  # 前n日低点
    for i in range(h.discard, len(k)):
        if (c[i] >= h[i]):
            self._add_buy_signal(k[i].datetime)
        elif (c[i] <= L[i]):
            self._add_sell_signal(k[i].datetime)


# 创建模拟交易账户进行回测，初始资金30万
my_tm = crtTM(init_cash=100000)

# my_mm = MM_Nothing()
# my_mm = MM_FixedCount(1000)
my_mm = DEMO_MM()

my_sg = crtSG(TurtleSG, {'n1': 20, 'n2': 10}, 'TurtleSG')
# 创建信号指示器（以5日EMA为快线，5日EMA自身的10日EMA作为慢线，快线向上穿越慢线时买入，反之卖出）
# my_sg = SG_Flex(EMA(C, n=5), slow_n=10)


# 创建交易系统并运行
sys = SYS_Simple(tm=my_tm, sg=my_sg, mm=my_mm)

sys.run(sm['sz000001'], Query(-150))

# 绘制系统信号
sys.plot()

k = sm['sz000001'].get_kdata(Query(-150))
c = CLOSE(k)
fast = SMA(c, 10)
slow = SMA(fast, 20)

# 绘制信号指示器使用两个指标
fast.plot(new=False)
slow.plot(new=False)

# 绘制资金收益曲线
x = my_tm.get_profit_curve(k.get_datetime_list(), Query.DAY)
x = PRICELIST(x)
x.plot()

# 回测统计
per = Performance()
print(per.report(my_tm, Datetime(datetime.today())))

my_tm.tocsv(sm.tmpdir())
