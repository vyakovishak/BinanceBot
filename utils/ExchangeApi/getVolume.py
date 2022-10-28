import asyncio
from datetime import datetime, timedelta
import pandas as pd
from aiohttp import ClientSession
from aiohttp.web_exceptions import HTTPError

badRequestCounter = 0


async def getVolume(tokenData, time="1m"):
    async with ClientSession() as session:
        print(await asyncio.gather(*[getTokenVolumes(symbol, time, session) for symbol in tokenData]))


def filterUIKlinesResponse(symbol, response):
    filteredData = {}
    data = []
    for tokenData in response:
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
    filteredData[symbol] = data
    return filteredData


async def getTokenData(symbol, time, session):
    params = {
        'limit': '100',
        'symbol': symbol,
        'interval': time,
    }
    url = "https://www.binance.com/api/v3/uiKlines"
    print("John is a dick!")
    try:
        response = await session.request(method='GET', url=url, params=params)
        response.raise_for_status()
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")
    response_json = await response.json()
    return response_json


async def getTokenVolumes(symbol, time, session):
    response = await getTokenData(symbol, time, session)
    chartData = filterUIKlinesResponse(symbol, response)
    totalVolume, youngestDate, oldest = await filterVolume(symbol, chartData)
    data = {"TotalVolume": totalVolume,
            "OlderTime": youngestDate,
            "YoungestDate": oldest}
    return data


async def filterVolume(symbol, chartData):
    date30 = (datetime.utcnow() - timedelta(minutes=60))
    filteredDate = []
    volumeDate = []
    for date in chartData[symbol]:
        if date["OpenTime"] > date30:
            filteredDate.append(date["OpenTime"])
            volumeDate.append(int(float(date["Volume"])))
    youngestDate = filteredDate[0]
    oldest = filteredDate[len(filteredDate) - 1]
    totalVolume = sum(volumeDate)
    return totalVolume, oldest, youngestDate


if __name__ == '__main__':
    pass
    asyncio.run(getVolume(["CHESSBTC", "CHESSBTC", "CHESSBTC", "CHESSBTC"]))
