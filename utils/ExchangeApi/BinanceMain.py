import asyncio
import json
import random
from datetime import datetime, timedelta
from urllib.error import HTTPError
import binance
import aiohttp
import pandas as pd
from aiohttp import ClientSession
from requests.auth import HTTPProxyAuth

from utils.ExchangeApi import pairsNames
from utils.ExchangeApi.Binance_Functions import main


class BinanceAPI:
    def __init__(self, pairs: list, time: str, userParameter: str):
        self.proxies = self.proxyLoader()
        self.pairs = pairs
        self.time = time
        self.userParameter = userParameter
        self.filteredData = None
        self.requestRespond = None
        self.pairSymbol = None
        self.URL = None
        self.requestParams = None
        self.finalData = []
        self.proxySatus = None
        self.badRequestCounter = 0

    async def getData(self):
        async with ClientSession() as session:
            # await asyncio.sleep(random.randrange(30, 60))
            await asyncio.gather(*[self.requestTokenData(pair, session) for pair in self.pairs])

        sorted(self.finalData)
        maybeIdontKnow = {}
        for pairDo in self.pairs[0]:
                for pairDone in self.finalData:
                    if pairDo == pairDone['symbol']:
                        maybeIdontKnow.update({"symbol": pairDone["symbol"],
                                               "price": pairDone["price"],
                                               "volume": pairDone["volume"],
                                               "quoteVolume": pairDone["quoteVolume"],
                                               "openTime": pairDone["openTime"],
                                               "closeTime": pairDone["closeTime"]})
                        break
        print(maybeIdontKnow)

    def setParameters(self):
        if self.userParameter == "ticker":
            self.URL = "https://www.binance.com/api/v3/ticker"
            self.requestParams = {
                'type': 'MINI',
                'symbols': str(self.pairSymbol).replace("'", '"').replace(" ", ""),
                'windowSize': self.time,
            }

    def respondCheck(self):
        if self.requestRespond is not None:
            if self.userParameter == "ticker":
                self.winTicker()
            elif self.userParameter == "UIKlines":
                self.filterUIKlinesResponse()
                self.filterVolume()

    def winTicker(self):
        for pair in self.requestRespond:
            self.finalData.append({"symbol": pair["symbol"],
                                   "price": pair["lastPrice"],
                                   "volume": pair["volume"],
                                   "quoteVolume": pair["quoteVolume"],
                                   "openTime": pd.to_datetime(pair["openTime"], unit='ms'),
                                   "closeTime": pd.to_datetime(pair["closeTime"], unit='ms')})

    def filterUIKlinesResponse(self) -> object:
        filteredData = {}
        data = []
        for tokenData in self.requestRespond:
            data.append({"OpenTime": pd.to_datetime(tokenData[0], unit='ms'),
                         "OpenPrice": tokenData[1],
                         "HighPrice": tokenData[2],
                         "LowPrice": tokenData[3],
                         "ClosePrice": tokenData[4],
                         "Volume": tokenData[5],
                         "CloseTime": pd.to_datetime(tokenData[6], unit='ms'),
                         "QuoteVolume": tokenData[7],
                         "TradesNumber": tokenData[8],
                         "BaseTokenVolume": tokenData[9],
                         "QuoteTokenVolume": tokenData[10]
                         })
        filteredData[self.pairSymbol] = data
        self.filteredData = filteredData
        totalVolume, oldest, youngestDate = self.filterVolume()
        self.finalData.append({self.pairSymbol: {"TotalVolume": totalVolume,
                                                 "OlderTime": youngestDate,
                                                 "YoungestDate": oldest}})

    def filterVolume(self):
        date30 = (datetime.utcnow() - timedelta(minutes=60))
        filteredDate = []
        volumeDate = []
        for date in self.filteredData[self.pairSymbol]:
            if date["OpenTime"] > date30:
                filteredDate.append(date["OpenTime"])
                volumeDate.append(int(float(date["Volume"])))
        youngestDate = filteredDate[0]
        oldest = filteredDate[len(filteredDate) - 1]
        totalVolume = sum(volumeDate)
        return totalVolume, oldest, youngestDate

    async def requestTokenData(self, pair, session):
        self.pairSymbol = pair
        self.setParameters()
        auth = aiohttp.BasicAuth("gbismarc", "zm6cg75gmr7l")
        session.proxies = await self.proxyHandel()
        if self.badRequestCounter < 1:
            try:
                response = await session.request(method='GET', url=self.URL, params=self.requestParams, auth=auth)
                response.raise_for_status()
                self.requestRespond = await response.json()
            except Exception as err:
                print(f"An error occurred: {err} waiting 30 secounds")
                self.badRequestCounter = self.badRequestCounter + 1
                await asyncio.sleep(30)
                await self.requestTokenData(pair, session)
            self.respondCheck()

    async def proxyHandel(self):
        counter = 0
        for proxy in list(self.proxies.keys()):
            if not self.proxies[proxy] > 10:
                # print(f"Using this proxy {proxy} and count is {self.proxies[proxy]}")
                self.proxies[proxy] = self.proxies[proxy] + 1
                return {"http": proxy}
            elif len(list(self.proxies.keys())) <= counter:
                print("Resetting proxy")
                for status in list(self.proxies.keys()):
                    self.proxies[status] = 0
                    await asyncio.sleep(15)
            counter = counter + 1

    @staticmethod
    def proxyLoader():
        with open("proxy.txt", "r") as p:
            proxies = p.readlines()
        proxiesDic = {}
        for proxy in proxies:
            splitedProxy = proxy.split(":")
            ip = splitedProxy[0]
            port = splitedProxy[1]
            proxiesDic.update({f"{ip}:{port}": 0})
        print(f"{len(proxies)} proxy loaded!")
        # print(proxiesDic)
        return proxiesDic


# pair = main()
# print(len(pair))
asyncio.run(BinanceAPI([['APEAUD', 'AUDIOUSDT', 'BTCUSDT', 'CHESSUSDT']], "30m", "ticker").getData())

trade = {
    "1": {
        "CHESSBTC": {"base": "BTC",
                     "quote": "CHEDD",
                     "price": "0.22"},
        "BTCAPE": {"base": "BTC",
                   "quote": "APE",
                   "price": "0.00022"},
        "APEUSDT": {"base": "USDT",
                    "quote": "APE",
                    "price": "1.0"}
    },
    "2": {
        "CHESSBTC": {"base": "BTC",
                     "quote": "CHEDD",
                     "price": "0.22"},
        "BTCAPE": {"base": "BTC",
                   "quote": "APE",
                   "price": "0.00022"},
        "APEUSDT": {"base": "USDT",
                    "quote": "APE",
                    "price": "1.0"}
    },
    "3": {
        "CHESSBTC": {"base": "BTC",
                     "quote": "CHEDD",
                     "price": "0.22"},
        "BTCAPE": {"base": "BTC",
                   "quote": "APE",
                   "price": "0.00022"},
        "APEUSDT": {"base": "USDT",
                    "quote": "APE",
                    "price": "1.0"}
    }
}
