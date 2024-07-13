import os
import random
import time
from time import sleep

from bitcoinlib.keys import Address
from tronpy import Tron
import eth_account
from tronpy.keys import PrivateKey
from web3 import Web3, EthereumTesterProvider
import bitcoinlib
from bitcoinlib.wallets import Wallet
import bitcoin
from web3 import Account

client = Tron()
global detection_num
import G

btcAddressBalanceUrl = "https://blockchain.info/q/addressbalance/"


def getWeb3():
    return Web3(Web3.HTTPProvider("https://mainnet.infura.io/v3/2e67be7f04864e658f14e856b19e0e86"))


def detectionAddress(input_private_key,reqBalance = False):
    address_new = client.generate_address(PrivateKey(bytes.fromhex(input_private_key)))
    private_key = address_new["private_key"]
    trxAddress = address_new["base58check_address"]
    ethAddress = Account.from_key(private_key).address
    btcAddress = Address(private_key, encoding='bech32', script_type='taproot').address  # p2wpkh
    address_new.update({"trxAddress": address_new.pop("base58check_address")})
    address_new.update({"ethAddress": ethAddress})
    address_new.update({"btcAddress": btcAddress})
    del address_new["public_key"]
    del address_new["hex_address"]
    #print(address_new)
    balance = 0
    try:
        balance +=  client.get_account_balance(trxAddress) if reqBalance else 0
    except:
        pass

    try:
        if reqBalance:
            w3 = getWeb3()
            if w3.is_connected():
                # ac = w3.eth.account.create()
                balance += w3.eth.get_balance(ethAddress)
                # print(ac.address, ac.key.hex(), balance_eth)
    except:
        pass

    if G.same_last_char(trxAddress, 4) or G.same_last_char(ethAddress, 6) or G.same_last_char(btcAddress,6) or balance > 0:
        print("入库",address_new,balance)
        G.BlockchainAddress.create(trxAddress=trxAddress,ethAddress=ethAddress,btcAddress=btcAddress, private_key=private_key, balance=balance)


def random_address(x):
    global detection_num
    detection_num = 0
    t1 = time.time()
    for i in range(x):
        private_key = bitcoin.random_key()
        detectionAddress(private_key)
        detection_num += 1
        if detection_num > 10000:
            G.BlockchainAddress.update(balance=G.BlockchainAddress.balance + detection_num).where(
                G.BlockchainAddress.id == 1).execute()
            detection_num = 0
            print(i)
        #sleep(1)


if __name__ == '__main__':
    print("********* block start ***********")
    s = ""
    for i in range(32):
        s += "00"
    print(s)
    #private_key = "19871206199112055201314520690123456789abcdef15818852008153630863"
    #detectionAddress(private_key)
    #private_key = bitcoin.random_key()
    #private_key = "3ae7b3bca3b479baa65eb53f8207d4ce01f0a7ec6a5fca877a3846074720d2e2"
    #btcAddress = Address(private_key, encoding='bech32', script_type='p2wpkh').address   #base58  bech32     p2wpkh  p2tr
    #btcAddress1 = Address(private_key, encoding='base58', script_type='p2pkh').address
    #print("private_key:", private_key)
    #print("btcAddress:", btcAddress,btcAddress1)  # bc1qsgfyumu5uajt8dk83frt6n7dngst389u0w0z2z

    random_address(1000000000)
    # detectionAddress()
