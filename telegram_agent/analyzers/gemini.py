# analyzers.py
from google import genai
import asyncio
import time
from google.genai.types import Content, Part, GenerateContentConfig, ThinkingConfig

from ..interfaces import AnalyzerInterface


class GeminiAnalyzer(AnalyzerInterface):
    def __init__(self, key: str):
        self.client = genai.Client(api_key=key)
        self.last_request_time = 0

    async def analyze(self, texts: list[str], prompt: str):
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time

        if time_since_last_request < 60:
            await asyncio.sleep(60 - time_since_last_request)

        self.last_request_time = time.time()
        
        contents = []
        # системная инструкция может быть
        contents.append(Content(role="model", parts=[Part(text=prompt)]))
        # предыдущие сообщения
        for t in texts:
            contents.append(Content(role="user", parts=[Part(text=t)]))

        resp = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents,
            config=GenerateContentConfig(
                thinking_config=ThinkingConfig(thinking_budget=0)
            )
        )
        return resp.text
