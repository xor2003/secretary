from telegram import Bot

from ..interfaces import Notifier


class TelegramNotifier(Notifier):
    def __init__(self, token, owner_id):
        self.bot = Bot(token=token)
        self.owner_id = owner_id

    async def notify(self, text):
        await self.bot.send_message(chat_id=self.owner_id, text=text)
