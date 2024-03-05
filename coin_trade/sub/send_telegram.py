from telegram import Bot

def send_telegram_message(bot_token, chat_id, message, loger= None):
    try:
        bot = Bot(token=bot_token)
        bot.send_message(chat_id=chat_id, text=message)
        return True
    except Exception as e:
        if loger: loger.info(f"send_telegram_message >> {e}")
        else: print(f"send_telegram_message >> {e}")
        return False