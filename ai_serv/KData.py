import time
import requests


# CF401 -> CF2401
# m2401 -> M2401
# rb2401 -> RB2401

# we may have rb2401 or CF401, or m2401 when we want to get info from sina.

# commodity part is 'rb', or 'm', or 'CF'.
# year is '24' or just '4'.
# long_code includes commodity, year and month.
# but CZCE's long_code is like CF401. It has just 1 digit in the year part.

# a long_code is the same as full_code when it has 2 digits in the year part.
# a long_code turns into a full_code
# when we add '2' to the beginning of the year part when it has just 1 digit.

# sina requires full_code and capitalize it as argument.


# -----------------------------------------------------------------------------
def get_commodity_code(long_code):
    # get 'rb' out of 'rb2401'
    # return  'rb'
    com_code = ''
    for char in long_code:
        try:
            int(char)
            break
        except ValueError:
            com_code += char
    return com_code


# -----------------------------------------------------------------------------
def get_full_code(long_code):
    # add '2' to MA301, make it MA2301, for CZCE only
    long_code = str.upper(long_code)
    com_c = get_commodity_code(long_code)
    ym = long_code[len(com_c):]

    if 3 == len(ym):
        full_code = ''.join([com_c, '2',ym])
    else:
        full_code = long_code

    return full_code


# -----------------------------------------------------------------------------
def get_sina_future_data(long_code, market="CF", adjust='0'):
    """
    期货的实时行情数据
    http://vip.stock.finance.sina.com.cn/quotes_service/view/qihuohangqing.html#titlePos_1
    :param symbol: 合约名称的字符串组合
    :type symbol: str
    :param market: CF 为商品期货
    :type market: str
    :param adjust: '1' or '0'; 字符串的 0 或 1
    :type adjust: str
    :return: 期货的实时行情数据
    :return type: list

    return
    [
        '"螺纹钢2401',   # 0 名字+到期年月
        '150000',       # 1 ?
        '3690.000',     # 2 开盘价
        '3717.000',     # 3 最高价
        '3684.000',     # 4 最低价
        '3690.000',     # 5 昨收
        '3690.000',     # 6 买一
        '3691.000',     # 7 卖一
        '3690.000',     # 8 最新价
        '3700.000',     # 9 结算价
        '3684.000',     # 10 昨结算
        '63',           # 11买一挂单量
        '10',           # 12 卖一挂单量
        '1697143.000',  # 13 持仓量
        '1021754',      # 14 成交量
        '沪',           # 15 交易所
        '螺纹钢',        # 16 商品品种
        '2023-09-28',   # 17 日期
        '1',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '3700.991',
        '0.000',
        '0',
        '0.000',
        '0',
        '0.000',
        '0',
        '0.000',
        '0',
        '0.000',
        '0',
        '0.000',
        '0',
        '0.000',
        '0',
        '0.000',
        '0"'
     ]
    """
    full_code = get_full_code(long_code)
    subscribe_list = ','.join(['nf_' + item.strip() for item in full_code.split(',')])
    url = f"https://hq.sinajs.cn/rn={round(time.time() * 1000)}&list={subscribe_list}"
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'no-cache',
        'Host': 'hq.sinajs.cn',
        'Pragma': 'no-cache',
        'Proxy-Connection': 'keep-alive',
        'Referer': 'http://vip.stock.finance.sina.com.cn/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
    }
    r = requests.get(url, headers=headers)

    # fut_data is like ["PVC2310  150132  6008.000  6125.000  6004.000  ...  0  0.000  0  0.000  0"]
    fut_data = [item.strip().split("=")[1].split(",") for item in r.text.split(";") if item.strip() != ""][0]
    return fut_data


# -----------------------------------------------------------------------------
if __name__ == '__main__':
    # 商品代码加上'0'是连续合约，比如 'rb0' 是螺纹钢连续合约
    print(get_sina_future_data('rb0'))