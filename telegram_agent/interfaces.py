from abc import ABC, abstractmethod
from typing import Any


class Messenger(ABC):
    @abstractmethod
    async def start(self):
        pass

    @abstractmethod
    async def fetch_unread(self) -> dict[str, tuple[list[str], int]]:
        pass

    @abstractmethod
    async def mark_read(self, chat_id: str, max_id: int):
        pass


class Email(ABC):
    """Interface for email connectors like IMAP"""

    @abstractmethod
    async def connect(self):
        pass

    @abstractmethod
    async def fetch_unread_emails(self) -> list[dict[str, Any]]:
        pass

    @abstractmethod
    async def mark_as_read(self, email_id: str):
        pass


class Analyzer(ABC):
    @abstractmethod
    def analyze(self, messages: list[str], prompt: str) -> str:
        pass


class Notifier(ABC):
    @abstractmethod
    async def notify(self, message: str):
        pass


class Reminder(ABC):
    @abstractmethod
    def create_reminder(self, summary: str, time):
        pass


class AnalyzerInterface(ABC):
    @abstractmethod
    def analyze(self, texts: list[str], prompt: str) -> str: ...
