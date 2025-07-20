import asyncio
import email
import imaplib
from email.header import decode_header
from typing import Any

from ..interfaces import Email


class IMAPConnector(Email):
    def __init__(self, config: dict[str, Any]):
        self.host = config.get("host")
        self.port = config.get("port", 993)
        self.username = config.get("username")
        self.password = config.get("password")
        self.mailbox = config.get("mailbox", "INBOX")
        self.connection = None

    async def connect(self):
        loop = asyncio.get_running_loop()
        self.connection = imaplib.IMAP4_SSL(self.host, self.port)
        await loop.run_in_executor(None, self.connection.login, self.username, self.password)
        await loop.run_in_executor(None, self.connection.select, self.mailbox)

    async def fetch_unread_emails(self) -> list[dict[str, Any]]:
        if not self.connection:
            await self.connect()

        loop = asyncio.get_running_loop()
        status, messages = await loop.run_in_executor(None, self.connection.search, None, "UNSEEN")
        if status != "OK":
            return []

        emails = []
        for num in messages[0].split():
            status, data = await loop.run_in_executor(None, self.connection.fetch, num, "(RFC822)")
            if status != "OK":
                continue

            raw_email = data[0][1]
            msg = email.message_from_bytes(raw_email)
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding or "utf-8")

            from_, encoding = decode_header(msg.get("From"))[0]
            if isinstance(from_, bytes):
                from_ = from_.decode(encoding or "utf-8")

            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    if content_type == "text/plain":
                        body = part.get_payload(decode=True).decode()
                        break
            else:
                body = msg.get_payload(decode=True).decode()

            emails.append({"id": num.decode(), "subject": subject, "from": from_, "body": body})
        return emails

    async def mark_as_read(self, email_id: str):
        if not self.connection:
            await self.connect()

        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, self.connection.store, email_id, "+FLAGS", "\\Seen")
