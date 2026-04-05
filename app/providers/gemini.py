from django.conf import settings
from google import genai

from .base import BaseAIService
from .enums import AIProvider, GeminiModel


class GeminiService(BaseAIService):

    def __init__(self, model: GeminiModel = GeminiModel.FLASH_3):
        if not settings.GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY not found. Please configure it via environment variables."
            )
        self.model = model
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)

    def get_chat_response(self, user_message: str, system_prompt: str = None) -> str:
        contents = user_message
        if system_prompt:
            contents = f"{system_prompt}\n\n{user_message}"
        response = self.client.models.generate_content(
            model=self.model, contents=contents
        )
        return response.text

    def get_provider_name(self) -> AIProvider:
        return AIProvider.GEMINI
