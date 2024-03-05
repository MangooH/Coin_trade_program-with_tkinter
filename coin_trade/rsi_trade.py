import threading
import time
from market.get_coin_price import get_all_coin_price
from order.market_order import sell_coin_now, buy_coin_now
from order.order_done_check import order_done_check
from sub.send_telegram import send_telegram_message
from indicator_files.get_rsi import cal_rsi
from lay_out import My_Layout


class Upbit_Auto(My_Layout):
    def __init__(self):
        super().__init__()

        self.today_money_send = False

    def start(self):
        self.running = True
        if not self.check_start():
            return

        self.list_file.insert(0, " ============================== ")
        self.list_file.insert(0, " ")
        self.list_file.insert(0, self.now_time + "매매를 시작합니다.")

        self.change_abled(False)

        thread_start = threading.Thread(target=self.sell_start, args=())
        thread_start.start()
        thread_start = threading.Thread(target=self.buy_start, args=())
        thread_start.start()

    # =================================================================================================

    def sell_start(self):  # 매도 담당영역
        failed_count = 0
        failed_msg = None

        while self.running:
            time.sleep(1)

            if failed_count > 10:
                self.list_file.insert(0, f"{self.now_time}{failed_msg}")
                self.list_file.itemconfig(0, {"fg": "orange"})
                send_telegram_message(
                    self.telegram_api, self.telegram_chat_id, failed_msg, self.logger
                )
                failed_count = 0

            now_sell_coin_list = [
                i for i in self.coin_list_dict if self.coin_list_dict[i]["vol"]
            ]  # 현재 매수 된 종목만 체크
            # print("sell_start 대상 >> ",now_sell_coin_list )

            for coin in now_sell_coin_list:  # 수동매도 감지하기
                if coin not in self.asset_dict:
                    self.list_file.insert(0, " ")
                    self.logger.info(f"{coin} 수동 매도 감지.")
                    self.list_file.insert(
                        0, f"{self.now_time}{coin} 수동매도 감지. 매매목록에서 제외 합니다."
                    )
                    self.list_file.itemconfig(0, {"fg": "orange"})
                    del self.coin_list_dict[coin]

            now_sell_coin_list = [
                i for i in self.coin_list_dict if self.coin_list_dict[i]["vol"]
            ]

            if not now_sell_coin_list:
                continue

            all_price_dict = get_all_coin_price(now_sell_coin_list, self.logger)

            if not all_price_dict:
                failed_count += 1
                failed_msg = "매매 대상 코인 현재가 조회에 문제가 있습니다."
                time.sleep(1)
                continue

            for coin_name in now_sell_coin_list:
                if self.running is False:
                    break
                vol = self.coin_list_dict[coin_name]["vol"]
                avg_price = self.coin_list_dict[coin_name]["avg_price"]

                profit_price = round(
                    avg_price * (1 + float(self.setting_info["profit_per"]) / 100), 4
                )
                loscut_price = round(
                    avg_price * (1 - float(self.setting_info["loscut_per"]) / 100), 4
                )
                now_price = all_price_dict[coin_name]

                sell_status = False

                now_per = round(((now_price / avg_price) - 1) * 100, 1)
                print(f"* 코인명 : {coin_name}, 현재 수익률 : {now_per}%")

                if now_price > profit_price:
                    msg = f"{self.now_time}{coin_name} 익절 조건 만족, 현재가: {now_price}, 평단가 : {avg_price}"
                    self.list_file.insert(0, msg)
                    self.list_file.itemconfig(0, {"fg": "red"})
                    self.logger.info(msg)
                    sell_status = True

                elif now_price < loscut_price:
                    msg = f"{self.now_time}{coin_name} 손절 조건 만족, 현재가: {now_price}, 평단가 : {avg_price}"
                    self.list_file.insert(0, msg)
                    self.list_file.itemconfig(0, {"fg": "blue"})
                    self.logger.info(msg)
                    sell_status = True

                if sell_status:  # 매도 조건 충족 이라면
                    sell_result = sell_coin_now(
                        coin_name,
                        vol,
                        self.UPBIT_ACCESS,
                        self.UPBIT_SECRET,
                        self.logger,
                    )
                    if not sell_result:
                        if now_price * float(vol) <= 5001:
                            msg = (
                                f"{self.now_time}{coin_name} 매도금액이 5000원 미만입니다. 목록에서 제외"
                            )
                            del self.coin_list_dict[coin_name]
                        else:
                            msg = f"{self.now_time}{coin_name} 매도에 문제가 있습니다."
                        self.logger.info(msg)
                        self.list_file.insert(0, msg)
                        self.list_file.itemconfig(0, {"fg": "orange"})
                        failed_count += 1
                        failed_msg = msg
                        continue

                    time.sleep(1)

                    result = self.order_result_return(
                        sell_result["uuid"], coin_name, "매도"
                    )

                    if result:
                        total_vol, avg = result
                        msg = f"{self.now_time}{coin_name} 매도 완료, 매도가: {avg}, 수량 : {total_vol}"
                        self.list_file.insert(0, msg)
                        self.logger.info(msg)
                        if self.telegram_api:
                            send_telegram_message(
                                self.telegram_api,
                                self.telegram_chat_id,
                                msg,
                                self.logger,
                            )

                    self.coin_list_dict[coin_name] = {"vol": 0, "avg_price": 0}
                    continue

    def buy_start(self):  # 매수 담당영역
        self.today_money_send = False

        failed_count = 0
        failed_msg = None

        money = int(self.setting_info["buy_money"])
        rsi_line = int(self.setting_info["rsi_line"])
        rsi_lenth = int(self.setting_info["rsi_lenth"])
        r_avg_lenth = int(self.setting_info["avg_rsi_lenth"])
        minus_in = float(self.setting_info["minus_in"])
        while self.running:
            time.sleep(1)

            if failed_count > 10:
                self.list_file.insert(0, f"{self.now_time}{failed_msg}")
                self.list_file.itemconfig(0, {"fg": "orange"})
                send_telegram_message(
                    self.telegram_api, self.telegram_chat_id, failed_msg, self.logger
                )
                failed_count = 0

            if not self.coin_list_dict:  # 모두 목록에서 제외되었을때
                self.change_abled("ON")
                msg = "매매대상 코인이 없습니다. 중지"
                self.list_file.insert(0, "")
                self.list_file.insert(0, f"{self.now_time}{msg}")
                continue

            now_buy_coin_list = [
                i for i in self.coin_list_dict if not self.coin_list_dict[i]["vol"]
            ]

            for coin in now_buy_coin_list:  # 수동매도 감지하기
                if coin in self.asset_dict:
                    self.list_file.insert(0, " ")
                    self.logger.info(f"{coin} 수동 매수 감지.")
                    self.list_file.insert(
                        0, f"{self.now_time}{coin} 수동매수 감지. 매매목록에서 제외 합니다."
                    )
                    self.list_file.itemconfig(0, {"fg": "orange"})
                    del self.coin_list_dict[coin]

            now_buy_coin_list = [
                i for i in self.coin_list_dict if not self.coin_list_dict[i]["vol"]
            ]

            if not now_buy_coin_list:
                continue

            for coin_name in now_buy_coin_list:
                time.sleep(0.5)
                if self.running is False:
                    break

                rsi_result = cal_rsi(
                    coin_name,
                    self.setting_info["bong_select"],
                    rsi_lenth,
                    r_avg_lenth,
                    self.logger,
                )

                if not rsi_result:
                    failed_count += 1
                    failed_msg = f"{coin_name} RSI 조회에 문제가 있습니다."
                    time.sleep(1)
                    continue

                before_rsi, now_rsi, now_rsi_avg = rsi_result

                if (
                    rsi_line >= now_rsi > before_rsi
                    and now_rsi > now_rsi_avg
                    and now_rsi_avg - now_rsi <= minus_in
                ):
                    if money > self.krw_balance:
                        msg = f"{self.now_time}{coin_name} 매수 시그널 발생되었지만 현금 잔액이 부족합니다."
                        print(msg)
                        if not self.today_money_send:
                            send_telegram_message(
                                self.telegram_api,
                                self.telegram_chat_id,
                                msg,
                                self.logger,
                            )
                            self.logger.info(msg)
                            self.today_money_send = True
                        continue

                    msg = f"{self.now_time}{coin_name} 매수 시그널, 직전 RSI: {before_rsi}, 현재 RSI: {now_rsi}, 평균 RSI : {now_rsi_avg}"
                    self.list_file.insert(0, "")
                    self.list_file.insert(0, msg)
                    self.logger.info(msg)

                    # 매수 함수 연결
                    buy_result = buy_coin_now(
                        coin_name,
                        money,
                        self.UPBIT_ACCESS,
                        self.UPBIT_SECRET,
                        self.logger,
                    )
                    if not buy_result:
                        msg = f"{self.now_time}{coin_name} 매수에 문제가 있습니다."
                        self.logger.info(msg)
                        self.list_file.insert(0, msg)
                        self.list_file.itemconfig(0, {"fg": "orange"})
                        failed_count += 1
                        failed_msg = msg
                        continue

                    time.sleep(1)
                    result = self.order_result_return(
                        buy_result["uuid"], coin_name, "매수"
                    )

                    if result:
                        total_vol, avg = result
                        msg = f"{self.now_time}{coin_name} 매수 완료, 매수가: {avg}, 수량 : {total_vol}"
                        self.list_file.insert(0, msg)
                        self.logger.info(msg)
                        if self.telegram_api:
                            send_telegram_message(
                                self.telegram_api,
                                self.telegram_chat_id,
                                msg,
                                self.logger,
                            )

                    else:
                        time.sleep(1)
                        if coin_name not in self.asset_dict:
                            msg = f"{coin_name} 자산 조회에서도 확인할 수 없음. 목록에서 제외"
                            self.list_file.insert(0, f"{self.now_time}{msg}")
                            self.list_file.itemconfig(0, {"fg": "orange"})
                            del self.coin_list_dict[coin_name]
                            self.logger.info(msg)
                            continue
                        else:
                            total_vol = self.asset_dict[coin_name]["balance"]
                            avg = self.asset_dict[coin_name]["avg_price"]

                    self.coin_list_dict[coin_name] = {
                        "vol": float(total_vol),
                        "avg_price": float(avg),
                    }
                    continue

    def order_result_return(self, order_id, coin_name, way):
        result = order_done_check(
            order_id, self.UPBIT_ACCESS, self.UPBIT_SECRET, self.logger
        )
        if not result:
            time.sleep(1)
            result = order_done_check(
                order_id, self.UPBIT_ACCESS, self.UPBIT_SECRET, self.logger
            )
            if not result:
                msg = f"{self.now_time}{coin_name} {way}는 정상적으로 이루어졌으나 {way} 결과 조회에 문제가 있습니다."
                self.logger.info(msg)
                self.list_file.insert(0, msg)
                self.list_file.itemconfig(0, {"fg": "orange"})

        return result


if __name__ == "__main__":
    app = Upbit_Auto()
    app.root.mainloop()
