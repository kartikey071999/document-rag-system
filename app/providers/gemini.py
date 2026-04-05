from django.conf import settings
from google import genai

from .base import BaseAIService


class GeminiService(BaseAIService):

    def __init__(self, api_key: str = None):
        self.api_key = api_key or settings.GEMINI_API_KEY
        if not self.api_key:
            raise ValueError(
                "GEMINI_API_KEY not found. Please configure it via environment variables or pass it directly."
            )
        self.client = genai.Client(api_key=self.api_key)

    def get_chat_response(self, user_message: str) -> str:
        response = self.client.models.generate_content(
            model="gemini-3-flash-preview", contents=user_message
        )
        return response.text

    def get_provider_name(self) -> str:
        return "Gemini"
