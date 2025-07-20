import asyncio
from datetime import datetime

from ..interfaces import Messenger


class ViberConnector(Messenger):
    def __init__(self, config):
        self.config = config
        self.messages = {
            "chat1": [
                {"text": "Hello from Viber!", "time": datetime.now().isoformat()},
                {"text": "Don't forget the meeting tomorrow", "time": datetime.now().isoformat()},
            ],
        }

    async def start(self):
        print("Viber connector started")
        await asyncio.sleep(1)  # Simulate connection delay

    async def fetch_unread(self):
        print("Fetching unread Viber messages")
        # Simulate returning unread messages
        return {"chat1": ([msg["text"] for msg in self.messages["chat1"]], len(self.messages["chat1"]))}

    async def mark_read(self, chat_id, max_id):
        print(f"Marked Viber chat {chat_id} as read up to message {max_id}")
