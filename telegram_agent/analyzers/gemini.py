# analyzers.py
from google import genai

from ..interfaces import AnalyzerInterface


class GeminiAnalyzer(AnalyzerInterface):
    def __init__(self, key):
        self.client = genai.Client(api_key=key)

    def analyze(self, texts, prompt):
        resp = self.client.models.generate_content(model="gemini-2.5-flash", contents=texts)
        return resp.text
