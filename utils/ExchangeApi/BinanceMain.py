import asyncio
from datetime import datetime, timedelta
from urllib.error import HTTPError

import pandas as pd
from aiohttp import ClientSession


class BinanceAPI:
    def __init__(self, pairs: list, time: str, userParameter: str):
        self.pairs = pairs
        self.time = time
        self.userParameter = userParameter
        self.filteredData = None
        self.requestRespond = None
        self.pairSymbol = None
        self.URL = None
        self.requestParams = None
        self.finalData = []

    async def getData(self):

        async with ClientSession() as session:
            await asyncio.gather(*[self.requestTokenData(pair, session) for pair in self.pairs])

        print(self.finalData)

    def setParameters(self):
        if self.userParameter == "volume":
            self.URL = "https://www.binance.com/api/v3/uiKlines"
            self.requestParams = {
                'limit': '100',
                'symbol': self.pairSymbol,
                'interval': self.time,
            }
        elif self.userParameter == "price":
            pass

    def respondCheck(self):
        if self.requestRespond is not None:
            self.filterUIKlinesResponse()
            self.filterVolume()
            
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

        try:
            response = await session.request(method='GET', url=self.URL, params=self.requestParams)
            response.raise_for_status()
        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"An error occurred: {err}")

        self.requestRespond = await response.json()
        self.respondCheck()


obj = BinanceAPI(["CHESSBTC", "CHESSBTC", "CHESSBTC"], "1m", "volume")
asyncio.run(obj.getData())

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
