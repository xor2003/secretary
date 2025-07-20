from abc import ABC, abstractmethod
from typing import Dict, List, Tuple


class Messenger(ABC):
    @abstractmethod
    async def start(self):
        pass

    @abstractmethod
    async def fetch_unread(self) -> Dict[str, Tuple[List[str], int]]:
        pass

    @abstractmethod
    async def mark_read(self, chat_id: str, max_id: int):
        pass


class Analyzer(ABC):
    @abstractmethod
    def analyze(self, messages: List[str], prompt: str) -> str:
        pass


class Notifier(ABC):
    @abstractmethod
    def notify(self, message: str):
        pass


class Reminder(ABC):
    @abstractmethod
    def create_reminder(self, summary: str, time):
        pass


class AnalyzerInterface(ABC):
    @abstractmethod
    def analyze(self, texts: List[str], prompt: str) -> str: ...
