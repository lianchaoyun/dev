from time import sleep
from tronpy import Tron
from lib.MysqlTool import *
import eth_account
from web3 import Web3, EthereumTesterProvider
client = Tron()
global w3
global detection_num

def getWeb3():
    global  w3
    w3 = Web3(Web3.HTTPProvider("https://mainnet.infura.io/v3/2e67be7f04864e658f14e856b19e0e86"))
    return w3

def detectionAddress():
    global detection_num
    detection_num=0
    while 1 == 1:
        address_new = client.generate_address()
        try:
            balance = client.get_account_balance(address_new["base58check_address"])
            print(address_new["base58check_address"], address_new["private_key"], balance)
            Address_new(address_new["base58check_address"], address_new["private_key"], "0")
        except:
            print(address_new["base58check_address"], address_new["private_key"], "0(无)")
            #Address_new(address_new["base58check_address"], address_new["private_key"], "0")
        w3 = getWeb3()
        if w3.is_connected():
            ac = w3.eth.account.create()
            balance_eth = w3.eth.get_balance(ac.address)
            if balance_eth > 0:
                print(ac.address, ac.key.hex(), balance_eth)
                Address_new(ac.address, ac.key.hex(), balance_eth)
            else:
                print(ac.address, ac.key.hex(), "0(无)")
                #Address_new(ac.address, ac.key.hex(), balance_eth)
        detection_num+=2
        if detection_num > 1000:
            Address_save_num(detection_num)
            detection_num=0
        sleep(5)

if __name__ == '__main__':
    print("********* block start ***********")
    detectionAddress()
    print("********* block end ***********")