from telegram import Bot
from interfaces import Notifier

class TelegramNotifier(Notifier):
    def __init__(self, token, chat_id):
        self.bot = Bot(token=token)
        self.chat_id = chat_id

    def notify(self, text):
        self.bot.send_message(chat_id=self.chat_id, text=text)
