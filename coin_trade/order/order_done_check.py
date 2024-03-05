import os
import jwt
import uuid
import hashlib
from urllib.parse import urlencode
import requests
import time


def order_done_check(uuids, ACCESS_KEY, SECRET_KEY, logger):  # 매도 주문이 체결되었는지 체크하는 함수
    query = {
        'uuid': uuids,
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
        res = requests.get("https://api.upbit.com/v1/order", params=query, headers=headers)
    except Exception as ex:
        logger.info(f"order_done_check err >> {ex}")
        return False

    if res.status_code == 200:
        if res.json()["state"] == "cancel" or res.json()["state"] == "done":
            total_vol = 0
            result_box = []
            for t in res.json()["trades"]:
                total_vol += float(t["volume"])
                result_box.append([float(t["volume"]), float(t["price"])])
            avg_price = 0
            for r in result_box:
                avg_price += (r[0] / total_vol) * r[1]

            return [round(total_vol, 8), round(avg_price, 4)]

        else:
            logger.info("주문 결과 문제 있음 > "+str(res.text))
            return False

    else:
        logger.info(f"order_done_check status_code >> {res.text}")
        return False

