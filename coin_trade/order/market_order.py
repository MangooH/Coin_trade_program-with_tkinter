import jwt, uuid, hashlib
from urllib.parse import urlencode
import requests


def buy_coin_now(coin_name, how_much,  ACCESS_KEY, SECRET_KEY, logger):
    query = {
        'market': coin_name,
        'side': 'bid',
        'price': how_much,
        'ord_type': 'price',
    }

    query_string = urlencode(query).encode()

    m = hashlib.sha512()
    m.update(query_string)
    query_hash = m.hexdigest()

    payload = {
        'access_key': ACCESS_KEY,
        'nonce': str(uuid.uuid4()),
        'query_hash': query_hash,
        'query_hash_alg': 'SHA512',
    }

    jwt_token = jwt.encode(payload, SECRET_KEY)
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}
    try:
        res = requests.post("https://api.upbit.com/v1/orders", params=query, headers=headers)
    except Exception as ex:
        logger.info("매수 주문 통신오류발생 " + str(ex))
        return False
    if res.status_code == 201:
        return res.json()

    else:
        logger.info("매수 주문 API 문제 발생 " + str(res.text))
        return False

def sell_coin_now(coin_name, volume, ACCESS_KEY, SECRET_KEY, logger):  # 지정가 매도 주문을 넣는 함수

    query = {
        'market': coin_name,
        'volume': volume,
        'side': 'ask',
        'ord_type': 'market',
    }

    query_string = urlencode(query).encode()

    m = hashlib.sha512()
    m.update(query_string)
    query_hash = m.hexdigest()

    payload = {
        'access_key': ACCESS_KEY,
        'nonce': str(uuid.uuid4()),
        'query_hash': query_hash,
        'query_hash_alg': 'SHA512',
    }

    jwt_token = jwt.encode(payload, SECRET_KEY)
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}
    try:
        res = requests.post("https://api.upbit.com/v1/orders", params=query, headers=headers)
    except Exception as ex:
        logger.info("매도 주문 통신오류발생 " + str(ex))
        return False
    if res.status_code == 201:
        return res.json()

    else:
        logger.info("매도 주문 API 문제 발생 " + str(res.text))
        return False
# start = time.time()
# print(sell_coin_instant("KRW-MANA",1.30718954))
# print("time :", time.time() - start)
