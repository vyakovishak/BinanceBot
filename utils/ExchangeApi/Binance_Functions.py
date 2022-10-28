import json
import os


def main():
    with open('pairs_response.json', 'r') as openfile:
        response_json = json.load(openfile)['data']

    target = "1INCH"

    exclude = []

    # showPairData(target, 1000, response_json)
    showSellOptions(target, response_json)

    # for trade in findBase(target, response_json):
    #     print(f"{'-' * 10} {trade['q']} {'-'*10}")
    #     showBuyOptions(trade['q'], response_json)
    #     print("\n")

    pairs = pair_route("CHESS", "APE", response_json)
    # pairs = pair_route("1INCH", "APE", response_json)
    # pairs = pair_route("BTC", "APE", response_json)
    # pairs = pair_route("1INCH", "PEOPLE", response_json)
    # pairs = pair_route("PEOPLE", "1INCH", response_json)
    print(pairs)

    # print(pair_route("PEOPLE", "1INCH", response_json, []))


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


def pair_route(start, end, entries, searched=[]):
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


def pair_route_old(start, end, entries, matched=[], searched=[]):
    if findMatch(start, end, entries):
        searched.append(start)
        searched.append(end)
        print(f"found match {start} -> {end}")
        matched.append(searched)  # Update our matched pairs
    else:
        for option in tradeOptions(start, entries):
            if option not in searched:
                searched.append(start)
                pair_route_old(option, end, entries)


def findMatch(start, end, entries):
    return any(end in sublist for sublist in tradeOptions(start, entries))


def tradeOptions(coin, entries):
    return [*set([trade['q'] for trade in findQuote(coin, entries) + findBase(coin, entries) if trade['q'] != coin]
                 +
                 [trade['b'] for trade in findQuote(coin, entries) + findBase(coin, entries) if trade['b'] != coin])]


if __name__ == '__main__':
    main()
