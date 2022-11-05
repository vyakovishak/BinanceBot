import asyncio
import random
from datetime import datetime, timedelta
from urllib.error import HTTPError

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

    def handel(self):
        async with ClientSession() as session:
            # await asyncio.sleep(random.randrange(30, 60))
            await asyncio.gather(*[self.requestHandel(pair, session) for pair in self.pairs])

    def requestHandel(self, pair, session):

        try:
            response = await session.request(method='GET', url=self.URL, params=self.requestParams, auth=auth)
            response.raise_for_status()
            self.requestRespond = await response.json()

        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"An error occurred: {err}")
