# connectors.py
from telethon import TelegramClient

from ..interfaces import Messenger


class TelegramConnector(Messenger):
    def __init__(self, cfg):
        self.client = TelegramClient("session.session", cfg["api_id"], cfg["api_hash"])
        self.chats = [c["chat_id"] for c in cfg.get("chats", [])]
        self.chat_groups = cfg.get("chat_groups", {})
        for group in self.chat_groups.values():
            self.chats.extend(group)
        self.bot_owner_id = cfg["bot_owner_id"]

    async def start(self):
        await self.client.start()

    async def fetch_unread(self):
        result = {}
        for chat_id in self.chats:
            try:
                entity = await self.client.get_entity(chat_id)
                messages = await self.client.get_messages(entity, limit=100)
                unread_messages = [msg.text for msg in messages if not msg.is_read and msg.text]
                if unread_messages:
                    result[chat_id] = (unread_messages, messages[0].id)
            except Exception as e:
                print(f"Could not fetch messages for chat {chat_id}: {e}")
        return result

    async def mark_read(self, chat_id, max_id):
        await self.client.read_chat_history(
            chat_id,
            max_id,
        )  # :contentReference[oaicite:1]{index=1}
