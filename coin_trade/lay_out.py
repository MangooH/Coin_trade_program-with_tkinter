import logging
import os
import pickle
import tkinter.font as tkFont
import tkinter.messagebox as msgbox
import tkinter.ttk as ttk
from tkinter import *
from market.main_coin_list import main_coin_list
import time
from wallet.asset import now_upbit_asset
from sub.send_telegram import send_telegram_message
import threading
from datetime import datetime
import certifi

certifi.where()


class My_Layout:
    def __init__(self):
        self.root = Tk()
        self.root.title("RSI 자동매매")  # 타이틀
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.logger = self.on_logging()

        self.root.geometry("600x570")
        content_frame = Frame(self.root)
        content_frame.pack(fill="x", padx=5, pady=1, ipady=1)

        self.target_coin_list = None
        self.setting_info = None

        self.now_time = None
        self.asset_dict = None

        self.UPBIT_ACCESS = None
        self.UPBIT_SECRET = None

        self.telegram_api = None
        self.telegram_chat_id = None

        self.krw_balance = None
        self.auth_setting_state = False

        self.running = True
        self.closing = True
        self.bong = None

        self.target_coin_list = None
        self.coin_list_dict = {}

        self.krw_balance_state = False

        content_frame = Frame(self.root)
        content_frame.pack(fill="x", padx=5, pady=1, ipady=1)

        # 프로그램 내 명령창 ###################################################
        scrollbar3 = Scrollbar(content_frame)
        scrollbar3.pack(side="right", fill="y")  # "y"로해야 위아래로 펼쳐짐.
        self.list_file = Listbox(
            content_frame,
            selectmode="extended",
            height=10,
            width=75,
            yscrollcommand=scrollbar3.set,
        )  # selectmode="extended" 다중선택여부
        self.list_file.pack(side="left", fill="both", expand=True)
        scrollbar3.config(command=self.list_file.yview)
        self.list_file.configure(font=("맑은 고딕", 10))
        self.list_file.insert(END, "   ")
        self.list_file.insert(END, "  1. 현재 RSI > 직전 RSI ")
        self.list_file.insert(END, "  2. 현재 RSI > 평균 RSI ")
        self.list_file.insert(END, "  3. 현재 RSI - 평균 RSI <= 입력값")
        self.list_file.insert(END, "  4. 모두 만족 시 매수 됩니다.")
        self.list_file.insert(
            END, "  5. 직전 RSI (직전 봉들 종가 기준 계산), 현재 RSI (직전 봉들 종가, 현재가 기준 계산)"
        )
        self.list_file.insert(END, "  6. 익절, 손절 기준은 매수가 대비 계산 됩니다.")
        ######################################################################

        fontStyle2 = tkFont.Font(family="Malgun Gothic", size=9, weight="bold")

        rsi_rate_frame = Frame(self.root)
        rsi_rate_frame.pack(fill="x", padx=5, pady=5, ipady=1)
        label = Label(rsi_rate_frame, text="  코인목록", font=fontStyle2)  # 라벨
        label.pack(side="left", padx=(10, 2), pady=5, ipady=4)
        self.target_coin = Entry(rsi_rate_frame, width=67)
        self.target_coin.pack(side="left", padx=5, pady=5, ipady=5)  # ipady 높이변경

        rsi_rate_frame = Frame(self.root)
        rsi_rate_frame.pack(fill="x", padx=5, pady=5, ipady=1)

        label = Label(rsi_rate_frame, text="  매수금액", font=fontStyle2)  # 라벨
        label.pack(side="left", padx=(10, 2), pady=5, ipady=4)

        self.buy_money = Entry(rsi_rate_frame, width=11)
        self.buy_money.pack(side="left", padx=5, pady=5, ipady=5)  # ipady 높이변경
        label = Label(rsi_rate_frame, text=" (코인 당)")  # 라벨
        label.pack(side="left", padx=(2, 2), pady=5, ipady=4)

        label = Label(rsi_rate_frame, text="분봉선택", font=fontStyle2)  # 라벨
        label.pack(side="left", padx=(9, 2), pady=5, ipady=4)

        values = [str(i) + "분봉" for i in [1, 3, 5, 10, 15, 30, 60, 240]] + ["1일봉"]
        self.bong_select = ttk.Combobox(
            rsi_rate_frame, width=9, height=10, values=values, state="readonly"
        )  # height 5는 보여주는 목록의 개수가 5개
        self.bong_select.pack(side="left", padx=(5, 5), pady=5, ipady=4)

        rsi_rate_frame = Frame(self.root)
        rsi_rate_frame.pack(fill="x", padx=5, pady=5, ipady=1)
        label = Label(
            rsi_rate_frame, text="  매수 시그널 1", font=fontStyle2, fg="green"
        )  # 라벨
        label.pack(side="left", padx=(5, 2), pady=5, ipady=4)
        values = [str(i) + "개" for i in range(1, 51, 1)]

        label = Label(rsi_rate_frame, text="현재 RSI-평균 RSI", font=fontStyle2)  # 라벨
        label.pack(side="left", padx=(10, 1), pady=5, ipady=4)

        self.minus_in = Entry(rsi_rate_frame, width=4)
        self.minus_in.pack(side="left", padx=5, pady=5, ipady=5)  # ipady 높이변경
        label = Label(rsi_rate_frame, text="이하", font=fontStyle2)  # 라벨
        label.pack(side="left", padx=(1, 2), pady=5, ipady=4)

        rsi_rate_frame = Frame(self.root)
        rsi_rate_frame.pack(fill="x", padx=5, pady=5, ipady=1)
        label = Label(
            rsi_rate_frame, text="  매수 시그널 2", font=fontStyle2, fg="green"
        )  # 라벨
        label.pack(side="left", padx=(5, 2), pady=5, ipady=4)

        label = Label(rsi_rate_frame, text="현재 RSI", font=fontStyle2)  # 라벨
        label.pack(side="left", padx=(9, 2), pady=5, ipady=4)

        values = [str(i) for i in range(5, 91, 1)]
        self.rsi_line = ttk.Combobox(
            rsi_rate_frame, width=6, height=10, values=values, state="readonly"
        )  # height 5는 보여주는 목록의 개수가 5개
        self.rsi_line.pack(side="left", padx=(5, 5), pady=5, ipady=4)
        label = Label(rsi_rate_frame, text="이하", font=fontStyle2)  # 라벨
        label.pack(side="left", padx=(1, 2), pady=5, ipady=4)

        label = Label(rsi_rate_frame, text="RSI 기간", font=fontStyle2)  # 라벨
        label.pack(side="left", padx=(9, 2), pady=5, ipady=4)

        values = [str(i) for i in range(25)]
        self.rsi_lenth = ttk.Combobox(
            rsi_rate_frame, width=4, height=10, values=values, state="readonly"
        )  # height 5는 보여주는 목록의 개수가 5개
        self.rsi_lenth.pack(side="left", padx=(5, 5), pady=5, ipady=4)

        label = Label(rsi_rate_frame, text="평균 RSI 기간", font=fontStyle2)  # 라벨
        label.pack(side="left", padx=(9, 2), pady=5, ipady=4)

        values = [str(i) for i in range(25)]
        self.avg_rsi_lenth = ttk.Combobox(
            rsi_rate_frame, width=4, height=10, values=values, state="readonly"
        )  # height 5는 보여주는 목록의 개수가 5개
        self.avg_rsi_lenth.pack(side="left", padx=(5, 5), pady=5, ipady=4)

        rsi_rate_frame = Frame(self.root)
        rsi_rate_frame.pack(fill="x", padx=5, pady=5, ipady=1)

        label = Label(rsi_rate_frame, text="  익절", font=fontStyle2, fg="red")  # 라벨
        label.pack(side="left", padx=(10, 2), pady=5, ipady=4)

        self.profit_per = Entry(rsi_rate_frame, width=9)
        self.profit_per.pack(side="left", padx=5, pady=5, ipady=5)  # ipady 높이변경

        label = Label(rsi_rate_frame, text="%", font=fontStyle2)  # 라벨
        label.pack(side="left", padx=(1, 2), pady=5, ipady=4)

        label = Label(rsi_rate_frame, text="  손절 -", font=fontStyle2, fg="blue")  # 라벨
        label.pack(side="left", padx=(19, 0), pady=5, ipady=4)

        self.loscut_per = Entry(rsi_rate_frame, width=9)
        self.loscut_per.pack(side="left", padx=0, pady=5, ipady=5)  # ipady 높이변경

        label = Label(rsi_rate_frame, text="%", font=fontStyle2)  # 라벨
        label.pack(side="left", padx=(1, 2), pady=5, ipady=4)

        fontStyle_asset = tkFont.Font(family="Malgun Gothic", size=10, weight="bold")
        btn_frame = Frame(self.root)
        btn_frame.pack(fill="x", padx=5, pady=1, ipady=2)
        btn_frame = Frame(self.root)
        btn_frame.pack(fill="x", padx=5, pady=1, ipady=2)
        self.krw_balance_label = Label(
            btn_frame, text="업비트 현금 잔액이 표시됩니다.", font=fontStyle_asset
        )
        self.krw_balance_label.pack(side="left", padx=(8, 2), ipady=2)

        btn_frame = Frame(self.root)
        btn_frame.pack(fill="x", padx=5, pady=1, ipady=2)
        self.auth_btn = Button(
            btn_frame, padx=3, pady=3, text="인증설정", command=self.auth_setting
        )
        self.auth_btn.pack(side="left", padx=(10, 5), pady=2, ipadx=2)

        self.start_btn = Button(
            btn_frame,
            padx=10,
            pady=5,
            text="시작",
            bg="black",
            fg="white",
            command=self.start,
        )  # pdax , pday 는 버튼의 여백 글자가 많아지면 x축이 길어짐.
        self.start_btn.pack(side="right", padx=(5, 15), pady=5, ipady=3, ipadx=20)
        self.stop_btn = Button(
            btn_frame, padx=10, pady=5, text="중지", command=self.stop
        )  # pdax , pday 는 버튼의 여백 글자가 많아지면 x축이 길어짐.
        self.stop_btn.pack(side="right", padx=10, pady=5, ipady=3, ipadx=20)

        data = self.load_auth_check()
        if data:
            self.UPBIT_ACCESS = data["upbit_access"]
            self.UPBIT_SECRET = data["upbit_secret"]
            self.telegram_api = data["telegram_api"]
            self.telegram_chat_id = data["telegram_chat_id"]
        self.load_dbs()
        thread_start = threading.Thread(target=self.now_time_update, args=())
        thread_start.start()
        thread_start_1 = threading.Thread(target=self.krw_balance_update, args=())
        thread_start_1.start()

    def check_start(self):
        self.target_coin_list = None
        self.setting_info = None

        if self.UPBIT_SECRET is None:
            msgbox.showwarning("인증설정", " 인증정보가 설정되지 않았습니다.")
            return ""

        upbit_coin_list = main_coin_list(self.logger)
        if not upbit_coin_list:
            msgbox.showwarning("API에러", " 업비트 코인 목록 조회에 문제가 있습니다.")
            return ""

        setting_info = self.save_dbs()
        target_coin = None
        for i in setting_info:
            if not setting_info[i]:
                msgbox.showwarning("입력확인", " 입력되지 않은 값이 존재합니다.")
                return ""
            if i == "target_coin":
                target_coin = [
                    "KRW-" + coin.upper().replace("KRW-", "")
                    for coin in setting_info[i].split(",")
                    if coin.replace(",", "")
                ]
                for coin in target_coin:
                    if coin not in upbit_coin_list:
                        msgbox.showwarning("코인확인", f"{coin} 업비트 원화마켓 코인 목록에 존재하지 않습니다.")
                        return ""
            if (
                i == "buy_money"
                or i == "minus_in"
                or i == "profit_per"
                or i == "loscut_per"
            ):
                try:
                    float(setting_info[i])
                except:
                    msgbox.showwarning("입력확인", f" 매수금액, 익절, 손절 등은 숫자만 입력 가능합니다.")
                    return ""
            if i == "buy_money":
                if float(setting_info[i]) < 5500:
                    msgbox.showwarning("매수금액", f"매수금액은 5500원 이상 입력 가능합니다.")
                    return ""
            # if i == "minus_in":
            #     if float(setting_info[i]) <= 0:
            #         msgbox.showwarning("시그널", f"현재 RSI - 평균 RSI 차는 0보다 커야 합니다.")
            #         return ""

        if (
            float(setting_info["loscut_per"]) <= 0
            or float(setting_info["profit_per"]) <= 0
        ):
            msgbox.showwarning("시그널", "익절 손절은 모두 양수로 입력해 주세요.")
            return ""

        if len(target_coin) * int(setting_info["buy_money"]) > self.krw_balance:
            msgbox.showwarning("현금 확인", "코인목록수*매수금액이 주문가능 잔액이 부족합니다.")
            return ""

        if "일봉" in self.bong_select.get():
            self.bong = [self.bong_select.get().replace("일봉", ""), "day"]
        else:
            self.bong = [self.bong_select.get().replace("분봉", ""), "minutes"]
        msg = "코인목록 : " + ",".join([coin.replace("KRW-", "") for coin in target_coin])
        msg += "\n\n 코인당 매수금액 : " + format(int(setting_info["buy_money"]), ",")
        msg += "\n\n 분봉선택 : " + setting_info["bong_select"]
        msg += f"\n\n RSI 기간 : {setting_info['rsi_lenth']} / 평균 RSI 기간 : {setting_info['avg_rsi_lenth']}"
        msg += f"\n\n 익절 : {setting_info['profit_per']}%, 손절 : -{setting_info['loscut_per']}%"
        MsgBox = msgbox.askquestion("작업시작", msg + "\n\n 맞습니까?")
        if MsgBox == "no":
            return False

        self.target_coin_list = target_coin
        self.setting_info = setting_info

        self.make_dict()

        return True

    def make_dict(self):
        self.coin_list_dict = {}
        print("self.asset_dict >>", self.asset_dict)
        for coin in self.target_coin_list:
            # print(coin)
            if coin in self.asset_dict:
                msg = f"{coin} 현재 보유 중입니다. 매매 목록에서 제외하시겠습니까? 미 제외 시 매도 대기합니다."
                MsgBox = msgbox.askquestion("코인확인", msg)
                if MsgBox == "yes":
                    self.logger.info(f"{coin} 목록 제외")
                if MsgBox == "no":
                    balance = self.asset_dict[coin]["balance"]
                    avg_price = self.asset_dict[coin]["avg_price"]
                    self.coin_list_dict[coin] = {"vol": balance, "avg_price": avg_price}
                continue
            else:
                self.coin_list_dict[coin] = {"vol": 0, "avg_price": 0}

        self.logger.info("시작 전 self.coin_list_dict >> " + str(self.coin_list_dict))

    def krw_balance_update(self):
        count = 0
        while self.closing:
            if self.UPBIT_ACCESS is None:
                time.sleep(1)
                continue

            result = now_upbit_asset(self.UPBIT_ACCESS, self.UPBIT_SECRET, self.logger)

            if not self.closing:
                break

            if not result:
                count += 1
                if count > 5:
                    self.list_file.insert(0, self.now_time + "업비트 자산 조회에 문제가 있습니다.")
                    self.list_file.itemconfig(0, {"fg": "red"})
                    count = 0
                time.sleep(1)
                continue

            count = 0
            self.asset_dict = result
            # print("self.asset_dict >> ",self.asset_dict)
            self.krw_balance = int(self.asset_dict["KRW"]["balance"])
            self.krw_balance_label.config(
                text="업비트 주문 가능 금액 :  " + format(self.krw_balance, ",")
            )

            for i in range(10):
                time.sleep(0.1)
                if not self.closing:
                    break

        self.krw_balance_state = True
        print("krw_balance_update 종료")

    def now_time_update(self):
        while self.closing:
            now_time = datetime.now()
            self.now_time = " (" + now_time.strftime("%m-%d %H:%M:%S") + ") "
            for i in range(4):
                time.sleep(0.25)
                if self.closing is False:
                    break
        print("now_time_update 종료.")

    def auth_setting(self):
        self.auth_setting_state = True
        self.auth_top = Toplevel(self.root)
        self.auth_top.title("인증설정")
        self.auth_top.resizable(False, False)
        self.auth_top.protocol("WM_DELETE_WINDOW", self.auth_top_closing)
        self.auth_top.attributes("-topmost", True)
        # self.auth_top.attributes("-topmost", True)
        fontStyle2 = tkFont.Font(family="Malgun Gothic", size=9, weight="bold")
        rsi_rate_frame = Frame(self.auth_top)
        rsi_rate_frame.pack(fill="x", padx=5, pady=1, ipady=1)
        label = Label(rsi_rate_frame, text=" 업비트 Access Key", font=fontStyle2)  # 라벨
        label.pack(side="left", padx=(13, 2), pady=3, ipady=1)
        upbit_acces_key = Entry(rsi_rate_frame, width=35)
        upbit_acces_key.pack(side="left", padx=(5, 20), pady=3, ipady=1)  # ipady 높이변경
        rsi_rate_frame = Frame(self.auth_top)
        rsi_rate_frame.pack(fill="x", padx=5, pady=1, ipady=1)
        label = Label(rsi_rate_frame, text=" 업비트 Secret Key", font=fontStyle2)  # 라벨
        label.pack(side="left", padx=(14, 2), pady=3, ipady=1)
        upbit_secret_key = Entry(rsi_rate_frame, width=35)
        upbit_secret_key.pack(side="left", padx=(5, 20), pady=3, ipady=1)  # ipady 높이변경
        rsi_rate_frame = Frame(self.auth_top)
        rsi_rate_frame.pack(fill="x", padx=5, pady=1, ipady=1)
        label = Label(rsi_rate_frame, text=" 텔레그램 API Key", font=fontStyle2)  # 라벨
        label.pack(side="left", padx=(14, 2), pady=3, ipady=1)
        tele_api_key = Entry(rsi_rate_frame, width=35)
        tele_api_key.pack(side="left", padx=(5, 20), pady=3, ipady=1)  # ipady 높이변경
        rsi_rate_frame = Frame(self.auth_top)
        rsi_rate_frame.pack(fill="x", padx=5, pady=1, ipady=1)
        label = Label(rsi_rate_frame, text=" 텔레그램 CHAT ID", font=fontStyle2)  # 라벨
        label.pack(side="left", padx=(14, 2), pady=3, ipady=1)
        chat_id = Entry(rsi_rate_frame, width=35)
        chat_id.pack(side="left", padx=(5, 20), pady=3, ipady=1)  # ipady 높이변경

        separator = ttk.Separator(self.auth_top, orient="horizontal")
        separator.pack(fill="x", ipady=1)

        rsi_rate_frame = Frame(self.auth_top)
        rsi_rate_frame.pack(fill="x", padx=5, pady=1, ipady=1)

        btn_frame = Frame(self.auth_top)
        btn_frame.pack(fill="x", padx=5, pady=1, ipady=5)
        save_auth_btn = Button(
            btn_frame,
            padx=10,
            pady=5,
            text="저장",
            bg="black",
            fg="white",
            command=lambda: self.save_auth(
                upbit_acces_key.get().strip(),
                upbit_secret_key.get().strip(),
                tele_api_key.get().strip(),
                chat_id.get().strip(),
            ),
        )  # pdax , pday 는 버튼의 여백 글자가 많아지면 x축이 길어짐.
        save_auth_btn.pack(side="right", padx=(10, 20), pady=5, ipady=3, ipadx=20)
        if self.UPBIT_ACCESS:
            upbit_acces_key.insert(END, self.UPBIT_ACCESS)
            upbit_secret_key.insert(END, self.UPBIT_SECRET)
        if self.telegram_api:
            tele_api_key.insert(END, self.telegram_api)
            chat_id.insert(END, self.telegram_chat_id)

    def auth_top_closing(self):
        self.auth_setting_state = False
        self.auth_top.destroy()

    def save_auth(self, api, secret, tele_api, chat_id):
        if api == "" or secret == "":
            msgbox.showwarning(
                "입력값 확인", "업비트 엑세스 또는 시크릿 중 입력되지 않은 값이 있습니다.", parent=self.auth_top
            )
            return ""

        if tele_api != "" and chat_id == "" or chat_id != "" and tele_api == "":
            msgbox.showwarning(
                "입력값 확인", "텔레그램 api키 또는 챗 아이디 중 입력되지 않은 값이 있습니다.", parent=self.auth_top
            )
            return ""

        data = {
            "upbit_access": api,
            "upbit_secret": secret,
            "telegram_api": tele_api,
            "telegram_chat_id": chat_id,
        }

        if not now_upbit_asset(api, secret, self.logger):
            msgbox.showwarning(
                "업비트 api키 확인",
                " 업비트 인증 확인에 문제가 있습니다. api 키, 시크릿키, ip 주소, 권한여부 등을 확인하세요.",
                parent=self.auth_top,
            )
            return ""

        if tele_api:
            msg = "텔레그램 전송 확인 메시지 입니다."
            if not send_telegram_message(tele_api, chat_id, msg, self.logger):
                msgbox.showwarning(
                    "텔레그램 확인",
                    " 텔레그램 전송에 문제가 있습니다. api, 챗 아이디를 확인하세요",
                    parent=self.auth_top,
                )
                return ""

        result = self.auth_check_and_save(data)
        if not result:
            msgbox.showwarning("저장에 어떤 문제가 있습니다.", parent=self.auth_top)
            return ""

        self.UPBIT_ACCESS = api
        self.UPBIT_SECRET = secret
        if tele_api:
            self.telegram_api = tele_api
            self.telegram_chat_id = chat_id

        msgbox.showwarning("저장완료", "저장 완료 되었습니다.", parent=self.auth_top)
        self.auth_top_closing()

    def auth_check_and_save(self, data):
        folder = os.getcwd() + "/config" + "/"
        if not os.path.exists(folder):
            os.makedirs(folder)

        try:
            with open(folder + "auth_check.db", "wb") as f:
                pickle.dump(data, f)

            self.logger.info("인증값 저장 완료")
            return True
        except Exception as e:
            self.logger.info(e)
            return False

    def load_auth_check(self):
        folder = os.getcwd() + "/config" + "/"
        if not os.path.exists(folder):
            os.makedirs(folder)
        try:
            with open(folder + "auth_check.db", "rb") as f:
                data = pickle.load(f)
                return data
        except:
            self.logger.info("기존 인증 데이터 없음")
            return {}

    def save_dbs(self):
        # print("저장 들어옴")
        folder = os.getcwd() + "/config" + "/"
        if not os.path.exists(folder):
            os.makedirs(folder)

        setting_info = {
            "target_coin": self.target_coin.get().strip().upper(),
            "buy_money": self.buy_money.get().strip(),
            "bong_select": self.bong_select.get().strip(),
            "minus_in": self.minus_in.get().strip(),
            "rsi_line": self.rsi_line.get().strip(),
            "rsi_lenth": self.rsi_lenth.get().strip(),
            "avg_rsi_lenth": self.avg_rsi_lenth.get().strip(),
            "profit_per": self.profit_per.get().strip(),
            "loscut_per": self.loscut_per.get().strip(),
        }
        print("setting_info >> ", setting_info)
        with open(folder + "basic_setting.db", "wb") as f:
            pickle.dump(setting_info, f)

        return setting_info

    def load_dbs(self):
        folder = os.getcwd() + "/config" + "/"
        if not os.path.exists(folder):
            os.makedirs(folder)
        try:
            with open(folder + "basic_setting.db", "rb") as f:
                setting_info = pickle.load(f)
        except:
            self.logger.info("기존 셋팅 데이터 없음")
            setting_info = {}

        if setting_info:
            self.target_coin.insert(END, setting_info["target_coin"])
            self.buy_money.insert(END, setting_info["buy_money"])
            self.bong_select.set(setting_info["bong_select"])
            self.minus_in.insert(END, setting_info["minus_in"])
            self.rsi_line.set(setting_info["rsi_line"])
            self.rsi_lenth.set(setting_info["rsi_lenth"])
            self.avg_rsi_lenth.set(setting_info["avg_rsi_lenth"])
            self.profit_per.insert(END, setting_info["profit_per"])
            self.loscut_per.insert(END, setting_info["loscut_per"])

        else:
            self.target_coin.insert(END, "BTC,ETH,XRP")
            self.buy_money.insert(END, "10000")
            self.bong_select.set("60분봉")
            self.minus_in.insert(END, "3")
            self.rsi_line.set("30")
            self.rsi_lenth.set("14")
            self.avg_rsi_lenth.set("9")
            self.profit_per.insert(END, "3")
            self.loscut_per.insert(END, "3")

    def change_abled(self, status):  # 버튼들 비활성화
        status_change = "disabled"
        if status == "ON":
            status_change = "normal"
            self.running = False
        self.target_coin.config(state=status_change)
        self.buy_money.config(state=status_change)
        self.bong_select.config(state=status_change)
        self.minus_in.config(state=status_change)
        self.rsi_line.config(state=status_change)
        self.rsi_lenth.config(state=status_change)
        self.avg_rsi_lenth.config(state=status_change)
        self.profit_per.config(state=status_change)
        self.loscut_per.config(state=status_change)
        self.start_btn.config(state=status_change)
        self.auth_btn.config(state=status_change)

    def stop(self):
        self.change_abled("ON")
        self.logger.info("중지 클릭됨")
        self.list_file.insert(0, " ")
        self.list_file.insert(0, self.now_time + " 중지되었습니다.")
        self.list_file.itemconfig(0, {"fg": "red"})

    # https://jh-bk.tistory.com/40
    # logger  에 대한 자세한 설명
    def on_logging(self):
        folder = os.getcwd() + "/config" + "/"
        if not os.path.exists(folder):
            os.makedirs(folder)
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s | %(message)s")
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        now_time = datetime.now().strftime("%Y_%m")
        file_handler = logging.FileHandler(
            folder + now_time + "_u_log.txt", encoding="utf-8"
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
        logger.addHandler(file_handler)
        return logger

    def on_closing(self):
        if self.start_btn["state"] == "disabled":
            msgbox.showwarning("중지 후 종료", "프로그램 중지 후 종료해 주세요.")
            return ""

        self.running = False
        self.closing = False
        count = 0
        while True:
            if count > 10:
                break
            if self.krw_balance_state:
                break
            else:
                count += 1
                time.sleep(0.5)
                continue
        self.save_dbs()
        self.logger.info("프로그램 종료")
        self.root.quit()
