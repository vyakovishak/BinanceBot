import json
import os
import re
from urllib import response

import requests


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
    return response.json()["data"]

def main():

    response_json = getBinanceData()

    target = "1INCH"

    exclude = []

    # showPairData(target, 1000, response_json)
    # print(tradeOptions("BTC", response_json))

    # for trade in findBase(target, response_json):
    #     print(f"{'-' * 10} {trade['q']} {'-'*10}")
    #     showBuyOptions(trade['q'], response_json)
    #     print("\n")

    # pairs = pair_route("CHESS", "APE", response_json)
    # pairs = pair_route("1INCH", "APE", response_json)
    # pairs = pair_route("BTC", "APE", response_json)
    # pairs = pair_route("1INCH", "PEOPLE", response_json)

    # pairs = pair_route("PEOPLE", "1INCH", response_json)
    # print(pairs)

    # print(pair_route("CHESS", "APE", response_json, []))
    # print(pair_route("1INCH", "APE", response_json, []))
    # print(pair_route("BTC", "APE", response_json, []))
    # print(pair_route("1INCH", "PEOPLE", response_json, []))
    # print(pair_route("PEOPLE", "1INCH", response_json,["PEOPLE"], []))
    # all_coins(response_json)

    # # Dictionary of Trade Options per Coin
    # coindb = {}
    # for coin in all_coins(response_json):
    #     coindb[coin] = tradeOptions(coin, response_json)

    # print(json.dumps(coindb))

    # print([f"{coin} - {tradeOptions(coin, response_json)}" for coin in all_coins(response_json)])
    # print(pair_route1("CHESS","APE", response_json))
    # pair_routes = pair_route("CHESS","APE", response_json)
    pair_routes = pair_route("APE", "CHESS", response_json)
    trade_list = listTrades(pair_routes, response_json)
    return trade_list


def listTrades(trades, response_json):
    tradePairs = []

    for trade in trades:
        current_trade = []
        for index in range(len(trade) - 1):
            coin_a = trade[index]
            coin_b = trade[index + 1]

            current_trade.append([e['s'] for e in response_json if coin_a in e['s'] and coin_b in e['s']][0])
            # current_trade.append(trade[index]+trade[index+1])
        tradePairs.append(current_trade)

    return tradePairs


def showBuyOptions(token, pairs):
    for trade in findQuote(token, pairs):
        print(f"BUYING 1 {trade['b']} Costs {trade['c']} {trade['q']}")


def showSellOptions(token, pairs):
    for trade in findQuote(token, pairs):
        print(f"SELLING 1 {trade['q']} Earns {1 / float(trade['c']):f} {trade['b']}")


def showPairData(token, coinAmount, pairs, count=0):
    # print([f"{trade['b']} -> {trade['q']}" for trade in findPairs(token, pairs)])

    new_pairs = [[item['b'], item['c'], coinAmount / float(item['c'])] for item in findPairs(token, pairs)]

    for pair in new_pairs:
        count += 1

        if count == 1:
            pass
        print(
            "\t" * count + f"{token} -> {pair[0]} \t| {coinAmount} {token} = {pair[2]} {pair[0]} \t | coin price {pair[1]} {token}")

        showPairData(pair[0], pair[2], pairs, count)
        count -= 1


def listCoinsSorted(response_json):
    for c in sorted([coin for coin in all_coins(response_json)], key=lambda x: len(findPairs(x, response_json)),
                    reverse=True):
        print(f"found {len(findPairs(c, response_json))} instances of {c}")


def all_coins(pairs):
    q_list = [entry['q'] for entry in pairs]
    b_list = [entry['b'] for entry in pairs]
    unique_list = [option for option in list(set(q_list + b_list))]
    return unique_list

    # print(unique_list)
    # print(f"availible coins: {len(unique_list)}")


def findPairs(target, pairs):
    return [entry for entry in pairs if target in [entry['b'], entry['q']]]


def findQuote(target, entries):
    return [entry for entry in entries if target == entry['q']]


def findBase(target, entries):
    return [entry for entry in entries if target == entry['b']]


def tradeOptions(target, targetPairs):
    q_list = [entry['q'] for entry in targetPairs]
    b_list = [entry['b'] for entry in targetPairs]

    return [option for option in q_list + b_list if option != target]


def pair_route(start, end, entries, mem=[], searched=[]):
    if end in tradeOptions(start, entries):
        return [[start, end]]
    else:
        for option in tradeOptions(start, entries):
            mem.append(option)
            if len(searched):
                if searched[len(searched) - 1] == start:
                    pass
                else:
                    searched.append(start)
            else:
                searched.append(start)

            if end in tradeOptions(option, entries):
                searched.append(option)
                searched.append(end)
            else:
                if option not in searched:
                    pair_route(option, end, entries, mem, searched)

        start_indexes = [i for i, x in enumerate(searched) if x == start]
        end_indexes = [i for i, x in enumerate(searched) if x == end]
        index_map = tuple(zip(start_indexes, end_indexes))

    # print("Raw Search")
    # print(searched)
    return [searched[index[0]:index[1] + 1] for index in index_map]  # +1 for slice proper indexing


def pair_route(start, end, entries, searched=[]):
    if end in tradeOptions(start, entries):
        return [[start, end]]
    else:
        for option in tradeOptions(start, entries):
            if end not in tradeOptions(option, entries):
                # print("2x search found no matches")
                for option2 in tradeOptions(option, entries):
                    if end not in tradeOptions(option2, entries):
                        # print("3x search found no matches")
                        for option3 in tradeOptions(option2, entries):
                            if end not in tradeOptions(option3, entries):
                                # print("4x search found no matches")
                                pass
                            else:
                                searched.extend([start, option, option2, option3, end])
                    else:
                        searched.extend([start, option, option2, end])
            else:
                print(f"Found match for {option}")
                # print(f"Found match for {option}: \n{tradeOptions(option, entries)}")
                searched.extend([start, option, end])

    start_indexes = [i for i, x in enumerate(searched) if x == start]
    end_indexes = [i for i, x in enumerate(searched) if x == end]
    index_map = tuple(zip(start_indexes, end_indexes))
    print(len(start_indexes))
    print(len(end_indexes))
    return [searched[index[0]:index[1] + 1] for index in index_map] if searched else []  # +1 for slice proper indexing


def pair_route(start, end, entries, searched=[]):
    if end in tradeOptions(start, entries):
        return [[start, end]]
    else:
        for option in tradeOptions(start, entries):
            if end not in tradeOptions(option, entries):
                # print("2x search found no matches")
                for option2 in tradeOptions(option, entries):
                    if end not in tradeOptions(option2, entries):
                        # print("3x search found no matches")
                        for option3 in tradeOptions(option2, entries):
                            if end not in tradeOptions(option3, entries):
                                # print("4x search found no matches")
                                pass
                            else:
                                searched.extend([start, option, option2, option3, end])
                    else:
                        searched.extend([start, option, option2, end])
            else:
                print(f"Found match for {option}")
                # print(f"Found match for {option}: \n{tradeOptions(option, entries)}")
                searched.extend([start, option, end])

    start_indexes = [i for i, x in enumerate(searched) if x == start]
    end_indexes = [i for i, x in enumerate(searched) if x == end]
    index_map = tuple(zip(start_indexes, end_indexes))
    print(len(start_indexes))
    print(len(end_indexes))
    return [searched[index[0]:index[1] + 1] for index in index_map] if searched else []  # +1 for slice proper indexing


def pair_route(start, end, entries, searched=[]):
    if end in tradeOptions(start, entries):
        return [[start, end]]
    else:
        for option in tradeOptions(start, entries):  # Dept 1
            if end not in tradeOptions(option, entries):
                # print("2x search found no matches")
                for option2 in [e for e in tradeOptions(option, entries) if e not in [start, option]]:  # Dept 2
                    if end not in tradeOptions(option2, entries):
                        # print("3x search found no matches")
                        for option3 in [e for e in tradeOptions(option2, entries) if
                                        e not in [start, option, option2]]:  # Dept 3
                            if end not in tradeOptions(option3, entries):
                                # print("4x search found no matches")
                                for option4 in [e for e in tradeOptions(option3, entries) if
                                                e not in [start, option, option2, option3]]:  # Dept 4
                                    if end not in tradeOptions(option4, entries):
                                        # print("4x search found no matches")
                                        pass
                                    else:
                                        searched.extend([start, option, option2, option3, option4, end])
                                        # break
                            else:
                                searched.extend([start, option, option2, option3, end])
                                # break
                    else:
                        searched.extend([start, option, option2, end])
                        # break
            else:
                print(f"Found match for {option}")
                # print(f"Found match for {option}: \n{tradeOptions(option, entries)}")
                searched.extend([start, option, end])

    start_indexes = [i for i, x in enumerate(searched) if x == start]
    end_indexes = [i for i, x in enumerate(searched) if x == end]
    index_map = tuple(zip(start_indexes, end_indexes))
    print(len(start_indexes))
    print(len(end_indexes))
    return [searched[index[0]:index[1] + 1] for index in index_map] if searched else []  # +1 for slice proper indexing


def pair_route_old(start, end, entries, searched=[]):
    if end in tradeOptions(start, entries):
        return [[start, end]]
    else:
        for option in tradeOptions(start, entries):
            searched.append(start)

            if end in tradeOptions(option, entries):
                searched.append(option)
                searched.append(end)
            else:
                if option not in searched:
                    pair_route(option, end, entries)

        start_indexes = [i for i, x in enumerate(searched) if x == start]
        end_indexes = [i for i, x in enumerate(searched) if x == end]
        index_map = tuple(zip(start_indexes, end_indexes))

    return [searched[index[0]:index[1] + 1] for index in index_map]  # +1 for slice proper indexing


def findMatch(start, end, entries):
    return any(end in sublist for sublist in tradeOptions(start, entries))


def tradeOptions(coin, entries):
    return [*set(
        [trade['q'] for trade in findQuote(coin, entries) + findBase(coin, entries) if trade['q'] != coin] + [trade['b']
                                                                                                              for trade
                                                                                                              in
                                                                                                              findQuote(
                                                                                                                  coin,
                                                                                                                  entries) + findBase(
                                                                                                                  coin,
                                                                                                                  entries)
                                                                                                              if trade[
                                                                                                                  'b'] != coin])]


