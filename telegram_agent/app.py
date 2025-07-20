"""Modular Messenger Summarizer App with Viber, Telegram, Google Calendar Support
"""

import asyncio
import json

from .analyzers.gemini import GeminiAnalyzer
from .connectors.telegram import TelegramConnector
from .notifiers.telegram import TelegramNotifier
from .reminders.google_calendar import GoogleCalendarReminder


class App:
    def __init__(self, cfg_path: str):
        cfg = json.load(open(cfg_path))

        self.cfg = cfg
        self.messengers = []

        if "telegram" in cfg["messengers"]:
            tg_cfg = cfg["messengers"]["telegram"]
            self.telegram = TelegramConnector(tg_cfg)
            self.notifier = TelegramNotifier(
                tg_cfg["bot_token"], tg_cfg["bot_owner_id"],
            )
            self.messengers.append(self.telegram)

        if "viber" in cfg["messengers"]:
            vb_cfg = cfg["messengers"]["viber"]
            from connectors.viber_connector import ViberConnector

            self.viber = ViberConnector(vb_cfg)
            self.messengers.append(self.viber)

        self.analyzer = GeminiAnalyzer(cfg["gemini_api_key"])
        self.prompts = {}

        for name, messenger in cfg["messengers"].items():
            for chat in messenger.get("chats", []):
                self.prompts[chat["chat_id"]] = chat.get(
                    "prompt_override", messenger["default_prompt"],
                )

        self.interval = cfg["schedule"].get("interval_minutes", 30) * 60

        if cfg.get("reminders", {}).get("enabled"):
            self.reminders = GoogleCalendarReminder(
                service_account_path=cfg["reminders"]["service_account_json"],
                calendar_id=cfg["reminders"]["calendar_id"],
            )
        else:
            self.reminders = None

    async def cycle(self):
        for messenger in self.messengers:
            await messenger.start()
            unread = await messenger.fetch_unread()
            for chat_id, (msgs, max_id) in unread.items():
                prompt = self.prompts.get(chat_id, "Summarize unread messages")
                summary = self.analyzer.analyze(msgs, prompt)
                self.notifier.notify(
                    f"Chat {chat_id} ({messenger.__class__.__name__}):\n{summary}",
                )
                await messenger.mark_read(chat_id, max_id)

    async def run(self):
        while True:
            await self.cycle()
            await asyncio.sleep(self.interval)


if __name__ == "__main__":
    asyncio.run(App("config.json", "secrets.json").run())
