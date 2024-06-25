# -*- coding: utf-8 -*-
import os
import platform
import time
import numpy as np
import requests
from browsermobproxy import Server
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import hashlib
sysstr = platform.system()
ha = {}
dicturl = {}
#print(np.linspace(1, 100, 100, endpoint=True,dtype=int))
#print(np.arange(1, 12, 1,dtype=int))
# https://github.com/mozilla/geckodriver/releases
# https://chromedriver.storage.googleapis.com/index.html?path=90.0.4430.24/
# yum install ./google-chrome-stable_current_x86_64.rpm
# cp ./ex/chromedriver     /usr/bin/chromedriver
def html(url, params,encoding):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
    }
    try:
        r = requests.get(url, headers=headers, timeout=30, verify=False, params=params)
        r.raise_for_status()
        # r.encoding = r.apparent_encoding
        # r.encoding = 'utf-8'
        r.encoding = encoding
        return r
    except Exception as err:
        return "爬取失败" + str(err)


def htmlbr(url, proxy, showWindow):
    try:
        chrome_options = Options()
        chrome_options.add_argument('--ignore-certificate-errors')
        if proxy is not None:
            chrome_options.add_argument('--proxy-server={}'.format(proxy))
        # chrome_options.binary_location = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
        if showWindow is not True:
            chrome_options.add_argument('--headless')

        chrome_options.add_argument('--disable-gpu')
        if sysstr == "Linux":
            chrome_options.add_argument('--no-sandbox')

            path = os.path.abspath(os.path.join(os.getcwd(), "../../../plugin/chromedriver_win32/chromedriver"))
            browser = webdriver.Chrome(executable_path=path, options=chrome_options)
        else:
            path = os.path.abspath(os.path.join(os.getcwd(), "../../plugin/chromedriver_win32/chromedriver.exe"))
            browser = webdriver.Chrome(executable_path=path, options=chrome_options)
        browser.get(url)  # 请求页面，会打开一个浏览器窗口
        time.sleep(4)
        v = browser  # 获得页面代码
        # browser.quit()  # 关闭浏览器
        return v
    except Exception as err:
        return "爬取失败" + str(err)


def useProxy():
    path = None
    if sysstr == "Windows":
        path = os.path.abspath(os.path.join(os.getcwd(),
                                            "../../plugin/browsermob-proxy-2.1.4/bin/browsermob-proxy.bat"))
    elif sysstr == "Linux":
        path = os.path.abspath(os.path.join(os.getcwd(), "../../plugin/browsermob-proxy-2.1.4/bin/browsermob-proxy"))
    else:
        path = os.path.abspath(os.path.join(os.getcwd(), "../../../plugin/ex/browsermob-proxy-2.1.4/bin/browsermob-proxy.bat"))

    bMPserver = Server(path)
    bMPserver.start()
    BMPproxy = bMPserver.create_proxy()
    BMPproxy.new_har("xianv", options={'xiannvContent': True, 'xiannvdeContent': True})
    return BMPproxy


# 读取Network json
# result_json = json.dumps(result,indent=4)
# with open("lagoujob.json","w",errors="igone") as f:
#     f.write(result_json)
# https://blog.csdn.net/lmt_fight/article/details/109300418




def stringtomd5(originstr):
    """将string转化为MD5"""
    signaturemd5 = hashlib.md5()
    signaturemd5.update(originstr)
    return signaturemd5.hexdigest()


# 保存字节图片
def saveImage(n, imgByte):
    dir = os.getcwd() + os.sep + "img" + os.sep + str(n) + '.jpg'
    fp = open(dir, 'wb')
    fp.write(imgByte)
    fp.close()
    print("下载完成" + str(n) + "张" + dir)


def save_obj():
    np.save('imgurls.npy', dicturl)


def load_obj():
    path = os.getcwd() + os.sep + 'imgurls.npy'
    read_dictionary = np.load(path, allow_pickle=True).item()
    for key in read_dictionary:
        print(str(read_dictionary[key]) + '  :  ' + key)


def meizi():
    bMPserver = useProxy()
    url = "http://papppp.com/moe.html"

    # url = "https://img.52ecy.cn/"
    # url = r"http://liilyy.com/?a=" + str(n)
    brow = htmlbr(url, bMPserver.proxy, True)
    while 1 == 1:
        print(brow)
        # brow.refresh()
        result = bMPserver.har
        for entry in result['log']['entries']:
            entry_url = entry['request']['url']
            if entry_url.startswith("https://tva1.sinaimg.cn/"):
                if entry_url in dicturl:
                    if dicturl[entry_url] > 0:
                        dicturl[entry_url] = dicturl[entry_url] + 1
                else:
                    dicturl[entry_url] = 1
                # print(entry_url)
        save_obj()
        load_obj()
        print("-------------------------------" + str(len(dicturl)) + "-------------------------------------")
        time.sleep(30)
def test1():
    pathimg = os.getcwd() + os.sep + '../../static/file/erciyuan/'
    path = os.getcwd() + os.sep + 'imgurls.npy'
    dicturl = np.load(path, allow_pickle=True).item()
    n = 1
    for key in dicturl:
        n += 1
        if dicturl[key] < 0:
            print("已经存在，跳过。"+str(dicturl[key]) + '  :  ' + key)
            continue
        r = html(key, {})
        c = r.content
        hasshstr = hash(key)
        extname = "png"
        if r.headers['Content-Type'] == 'image/jpeg':
            extname = "jpg"
        filepath = pathimg + os.sep + str(hasshstr) + "."+extname
        with open(filepath, "wb+") as f:
            f.write(c)
        dicturl[key] = - dicturl[key]
        save_obj()
        load_obj()
        print("下载第" + str(n) + "张"+str(dicturl[key]) + '  :  ' + key)
        time.sleep(1)
# if __name__ == '__main__':
#    path = os.getcwd() + os.sep + 'imgurls.npy'
#    dicturl = np.load(path, allow_pickle=True).item()
#    meizi()



