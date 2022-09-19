import json
import os

import requests


class Binance:
    def __init__(self, tokenA: str = None,
                 tokenB: str = "USDT",
                 userDollarAmount: int = 1000,
                 deepDive: int = 1,
                 crossExchangeMode: bool = False,
                 proxy: str = False):

        self.proxy = proxy
        self.crossExchangeMode = crossExchangeMode
        self.deepDive = deepDive
        self.userDollarAmount = userDollarAmount
        self.tokenB = tokenB
        self.tokenA = tokenA

    @staticmethod
    def getBinanceData():
        headers = {
            'Host': 'www.binance.com',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36',
            'content-type': 'application/json',
            'lang': 'en',
            'clienttype': 'web',
            'accept': '*/*',
            'sec-gpc': '1',
            'accept-language': 'en-US,en;q=0.9',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
        }
        params = {
            'includeEtf': 'true',
        }
        response = requests.get('https://www.binance.com/bapi/asset/v2/public/asset-service/product/get-products',
                                params=params, headers=headers)
        return response.json()

    def findPairs(self, target, pairs):
        matches = [entry for entry in pairs if target in [entry['q'], entry['b']]]
        return matches

    def findQuote(self, target, entries):
        return [entry for entry in entries if target == entry['q']]

    def findBase(self, target, entries):
        return [entry for entry in entries if target == entry['b']]

    def displayCoinData(self, item, token):
        return f"{token} -> {item[0]} \t| {item[1]} {token} = {item[2]} {item[0]} \t | coin price {item[1]} {token}"

    def showPairData(self, token, coinAmount, pairs, count=0):
        new_pairs = [[item['b'], item['c'], coinAmount / float(item['c'])] for item in binance.findPairs(token, pairs)
                     if item['b'] != token]
        for pair in new_pairs:
            count += 1
            if count == 3:
                pass
            print(
                "\t" * count + f"{token} -> {pair[0]} \t| {coinAmount} {token} = {pair[2]} {pair[0]} \t | coin price {pair[1]} {token}")

            binance.showPairData(pair[0], pair[2], pairs, count)
            count -= 1


binance = Binance()
binance_response = binance.getBinanceData()['data']
original_pairs = [[item['b'], item['c'], binance.userDollarAmount / float(item['c'])] for item in
                  binance.findPairs(binance.tokenB, binance_response) if item['b'] != binance.tokenB]

binance.showPairData(binance.tokenB, binance.userDollarAmount, binance_response)

