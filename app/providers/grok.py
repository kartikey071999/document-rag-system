from __future__ import annotations

from typing import TYPE_CHECKING

from django.conf import settings

from .base import BaseAIService
from .enums import AIProvider, GrokModel

if TYPE_CHECKING:
    from openai import OpenAI


class GrokService(BaseAIService):

    def __init__(self, api_key: str = None, model: GrokModel = GrokModel.GROK_BETA):
        self.api_key = api_key or getattr(settings, "XAI_API_KEY", None)
        if not self.api_key:
            raise ValueError(
                "XAI_API_KEY not found. Please configure it via environment variables or pass it directly."
            )
        self.model = model

        from openai import OpenAI

        self.client = OpenAI(api_key=self.api_key, base_url="https://api.x.ai/v1")

    def get_chat_response(self, user_message: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": user_message}],
        )
        return response.choices[0].message.content

    def get_provider_name(self) -> AIProvider:
        return AIProvider.GROK
