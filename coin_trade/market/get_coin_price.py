import requests
import time


def get_all_coin_price(coin_list, logger):
    coins = ",".join(coin_list)

    url = "https://api.upbit.com/v1/ticker"

    querystring = {"markets": coins}

    headers = {"Accept": "application/json"}
    try:
        response = requests.request("GET", url, headers=headers, params=querystring)

    except Exception as ex:
        logger.info("get_all_coin_price >> "+str(ex))
        return False

    if response.status_code == 200:
        pass
    else:
        logger.info("get_all_coin_price status_code >> " + str(response.text))
        return False

    data = response.json()
    return_dict = {}
    for i in data:
        return_dict[i["market"]] = float(i["trade_price"])
    # print(return_dict)
    return return_dict

# print(get_all_coin_price(['KRW-BTC','KRW-ETH'], ""))