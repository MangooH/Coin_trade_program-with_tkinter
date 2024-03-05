import requests
import pandas as pd
from datetime import datetime


def rsi_calc(ohlc: pd.DataFrame, period):
    ohlc["close"] = ohlc["close"]
    delta = ohlc["close"].diff()
    gains, declines = delta.copy(), delta.copy()
    gains[gains < 0] = 0
    declines[declines > 0] = 0

    _gain = gains.ewm(com=(period - 1), min_periods=period).mean()
    _loss = declines.abs().ewm(com=(period - 1), min_periods=period).mean()

    RS = _gain / _loss
    return pd.Series(100 - (100 / (1 + RS)), name="RSI")


def rsi_avg_calc(ohlc: pd.DataFrame, rsi_period):
    return ohlc["RSI"].rolling(window=rsi_period).mean()


def cal_rsi(coin_name, bong_type, rsi_lenth, rsi_avg_lenth, logger):  # rsi
    if bong_type == "1일봉":
        url = "https://api.upbit.com/v1/candles/days"
    else:
        minutes = bong_type.replace("분봉", "")
        url = f"https://api.upbit.com/v1/candles/minutes/{minutes}"

    querystring = {"market": coin_name, "count": "200"}  # 최근 200분 데이터 호출
    try:
        response = requests.request("GET", url, params=querystring)

    except Exception as e:
        logger.info("업비트 cal_rsi 통신오류 " + str(e))
        return False

    if response.status_code == 200:
        pass

    else:
        logger.info(f"업비트 cal_rsi status_code >> {response.text} ")
        return False

    data_info = []
    data = response.json()
    # ['High', "Low", "close"]
    for i in data[::-1]:
        # print(i)
        data_info.append([i["high_price"], i["low_price"], i["trade_price"]])
    columns = ["High", "Low", "close"]
    df = pd.DataFrame(data_info, columns=columns)

    if len(df["close"]) < rsi_lenth or len(df["close"]) < rsi_avg_lenth:
        logger.info(f"{coin_name} rsi 데이터의 기간이 짧습니다. 기간을 변경하거나 코인을 교체하세요.")
        return False

    df["RSI"] = rsi_calc(df, rsi_lenth)
    df["RSI_avg"] = rsi_avg_calc(df, rsi_avg_lenth)
    before_rsi = round(df["RSI"].iloc[-2], 2)
    now_rsi = round(df["RSI"].iloc[-1], 2)
    before_rsi_avg = round(df["RSI_avg"].iloc[-2], 2)
    now_rsi_avg = round(df["RSI_avg"].iloc[-1], 2)
    minus_val = round(now_rsi_avg - now_rsi, 2)
    print(
        f"코인명 : {coin_name}, 직전 RSI : {before_rsi}, 현재 RSI : {now_rsi}, 평균 RSI : {now_rsi_avg}, 차이 : {minus_val}"
    )

    return [before_rsi, now_rsi, now_rsi_avg]
    #
    # print(now_time, " ", coin_name, " >>  RSI: ", rsi)
    # return rsi


# cal_rsi("KRW-XRP", "240",14,9, "")
