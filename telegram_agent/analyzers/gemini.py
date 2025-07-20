# analyzers.py
import google.generativeai as genai

from ..interfaces import AnalyzerInterface


class GeminiAnalyzer(AnalyzerInterface):
    def __init__(self, key):
        genai.configure(api_key=key)

    def analyze(self, texts, prompt):
        resp = genai.generate_content(
            model="gemini-1.5-flash", contents=[prompt] + texts,
        )
        return resp.text
