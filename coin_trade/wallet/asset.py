import time
import jwt  # 업비트 매매관련 라이브러리
import requests  # api 호출 라이브러리
import uuid

def now_upbit_asset(access_key, secret_key, logger):
    count = 0
    while True:
        count += 1

        payload = {
            'access_key': access_key,
            'nonce': str(uuid.uuid4()),
        }
        jwt_token = jwt.encode(payload, secret_key)
        authorize_token = 'Bearer {}'.format(jwt_token)
        headers = {"Authorization": authorize_token}

        try:
            res = requests.get("https://api.upbit.com/v1/accounts", headers=headers)
            data = res.json()
        except Exception as ex:
            if count > 3:
                msg = "now_upbit_asset 서버오류>> " + str(ex)
                logger.info(msg)
                return False
            time.sleep(0.5)
            continue

        if res.status_code != 200:
            logger.info(str(res.text))
            return False

        asset_dict = {}

        for co in data:
            # print(co)
            if co["currency"] == "KRW":
                balance = float(co['balance'])  # 가용가능한 현금자산
                lock = float(co['locked'])  # 주문중인 현금자산
                asset_dict["KRW"] = {"balance": balance, "lock": lock}
            else:
                if co["unit_currency"] == "KRW":
                    name = "KRW-" + co["currency"]

                    balance = float(co['balance'])  # 매도 가능한 수량
                    if balance == 0:
                        continue
                    lock = float(co['locked'])  # 매도 주문중인 수량
                    avg_buy_price = float(co["avg_buy_price"])
                    asset_dict[name] = {"balance": balance, "lock": lock, "avg_price": avg_buy_price}

        if not asset_dict:
            msg = "자산이 없음 " + str(data)
            return False

        # print("asset_dict >>", asset_dict)
        return asset_dict