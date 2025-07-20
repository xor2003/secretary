# connectors.py
from telethon import TelegramClient

from ..interfaces import Messenger


class TelegramConnector(Messenger):
    def __init__(self, cfg):
        self.client = TelegramClient("session", cfg["api_id"], cfg["api_hash"])
        self.chats = [c["chat_id"] for c in cfg["chats"]]

    async def start(self):
        await self.client.start()

    async def fetch_unread(self):
        result = {}
        async for dialog in self.client.iter_dialogs():
            if dialog.id in self.chats:
                msgs = await self.client.get_messages(dialog.id, limit=100)
                unread = [m.text for m in msgs if not m.is_read and m.text]
                if unread:
                    result[dialog.id] = (unread, msgs[0].id)
        return result

    async def mark_read(self, chat_id, max_id):
        await self.client.read_chat_history(
            chat_id, max_id,
        )  # :contentReference[oaicite:1]{index=1}
