from django.conf import settings
from openai import OpenAI

from .base import BaseAIService
from .enums import AIProvider, OpenAIModel


class OpenAIService(BaseAIService):

    def __init__(self, model: OpenAIModel = OpenAIModel.GPT_4O_MINI):
        if not getattr(settings, "OPENAI_API_KEY", None):
            raise ValueError(
                "OPENAI_API_KEY not found. Please configure it via environment variables."
            )
        self.model = model
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def get_chat_response(self, user_message: str, system_prompt: str = None) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": user_message})
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
        )
        return response.choices[0].message.content

    def get_provider_name(self) -> AIProvider:
        return AIProvider.OPENAI
