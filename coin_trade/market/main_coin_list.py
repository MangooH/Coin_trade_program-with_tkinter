

import requests
import time


def main_coin_list(logger):  # 업비트 원화 코인 목록 조회, 서버지연 등 발생시 최대 counts만큼 실행, 인자 없을 시 기본 5회
    count = 0
    while True:
        count += 1

        url = "https://api.upbit.com/v1/market/all?isDetails=true"

        querystring = {"isDetails": "false"}
        try:
            response = requests.request("GET", url, params=querystring)
        except Exception as ex:
            if count > 3:
                logger.info("main_coin_list >> "+str(ex))
                return False
            time.sleep(0.5)
            continue

        if response.status_code == 200:
            pass
        else:
            if count > 3:
                logger.info("main_coin_list status_code>> "+response.text)
                return False
            time.sleep(0.5)
            continue

        coins = response.json()

        coin_symbol = []

        for i in coins:  # 조회한 코인을 코인박스에 보관
            if "KRW-" in i["market"]:  #원화마켓 코인만 리스트에 추가
                coin_symbol.append(i["market"])

        if not coin_symbol:
            msg = str("코인 목록 데이터가 없음. >> "+str(response.text))
            logger.info(msg)
            return False

        return coin_symbol

# print(main_coin_list(""))
