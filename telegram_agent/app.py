"""Modular Messenger Summarizer App with Viber, Telegram, Google Calendar and IMAP Support"""

import asyncio
import json

from .analyzers.gemini import GeminiAnalyzer
from .connectors.imap import IMAPConnector
from .connectors.telegram import TelegramConnector
from .notifiers.telegram import TelegramNotifier
from .reminders.google_calendar import GoogleCalendarReminder


class App:
    def __init__(self, config_path: str, secrets_path: str):
        with open(config_path) as f:
            cfg = json.load(f)
        with open(secrets_path) as f:
            secrets = json.load(f)

        self.cfg = cfg
        self.secrets = secrets
        self.messengers = []
        self.emails = []

    async def init(self):
        # Initialize messengers
        if "telegram" in self.cfg["messengers"]:
            tg_cfg = self.cfg["messengers"]["telegram"]
            # Merge with secrets
            if "telegram" in self.secrets:
                tg_cfg.update(self.secrets["telegram"])
            self.telegram = TelegramConnector(tg_cfg)
            self.notifier = TelegramNotifier(
                tg_cfg["bot_token"], tg_cfg["bot_owner_id"],
            )
            self.messengers.append(self.telegram)

        if "viber" in self.cfg["messengers"]:
            vb_cfg = self.cfg["messengers"]["viber"]
            from .connectors.viber import ViberConnector

            self.viber = ViberConnector(vb_cfg)
            self.messengers.append(self.viber)

        # Initialize email connectors
        if "emails" in self.cfg:
            for email_type, email_cfg in self.cfg["emails"].items():
                if email_type == "imap":
                    # Merge with secrets
                    if "imap" in self.secrets:
                        email_cfg.update(self.secrets["imap"])
                    self.imap = IMAPConnector(email_cfg)
                    self.emails.append(self.imap)

        self.analyzer = GeminiAnalyzer(self.secrets["gemini_api_key"])
        self.prompts = {}

        # Load prompts for messengers
        for name, messenger in self.cfg["messengers"].items():
            for chat in messenger.get("chats", []):
                default_prompt = messenger.get("default_prompt", "")
                custom_prompt = chat.get("prompt_override", "")
                self.prompts[chat["chat_id"]] = f"{default_prompt}\n{custom_prompt}".strip()

        # Load prompts for emails
        if "emails" in self.cfg:
            for email_type, email_cfg in self.cfg["emails"].items():
                default_prompt = email_cfg.get("default_prompt", "")
                self.prompts[email_type] = default_prompt

        self.interval = self.cfg["schedule"].get("interval_minutes", 30) * 60

        if self.cfg.get("reminders", {}).get("enabled"):
            self.reminders = GoogleCalendarReminder(
                service_account_path=self.cfg["reminders"]["service_account_json"],
                calendar_id=self.cfg["reminders"]["calendar_id"],
            )
        else:
            self.reminders = None

    async def process_emails(self):
        for email_conn in self.emails:
            await email_conn.connect()
            emails = await email_conn.fetch_unread_emails()
            for email in emails:
                prompt = self.prompts.get("imap", "Summarize this email")
                summary = self.analyzer.analyze([email["body"]], prompt)
                await self.notifier.notify(
                    f"Email from {email['from']} (IMAP):\nSubject: {email['subject']}\nSummary: {summary}",
                )
                await email_conn.mark_as_read(email["id"])

    async def cycle(self):
        # Process messengers
        for messenger in self.messengers:
            await messenger.start()
            unread = await messenger.fetch_unread()
            for chat_id, (msgs, max_id) in unread.items():
                prompt = self.prompts.get(chat_id, "Summarize unread messages.")
                summary = self.analyzer.analyze(msgs, prompt)
                await self.notifier.notify(
                    f"Chat {chat_id} ({messenger.__class__.__name__}):\n{summary}",
                )
                await messenger.mark_read(chat_id, max_id)

        # Process emails
        if self.emails:
            await self.process_emails()

    async def run(self):
        await self.init()
        while True:
            await self.cycle()
            await asyncio.sleep(self.interval)


if __name__ == "__main__":
    app = App("config.json", "secrets.json")
    asyncio.run(app.run())
