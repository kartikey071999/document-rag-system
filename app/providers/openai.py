from __future__ import annotations

from typing import TYPE_CHECKING

from django.conf import settings

from .base import BaseAIService
from .enums import AIProvider, OpenAIModel

if TYPE_CHECKING:
    from openai import OpenAI


class OpenAIService(BaseAIService):

    def __init__(self, api_key: str = None, model: OpenAIModel = OpenAIModel.GPT_4O_MINI):
        self.api_key = api_key or getattr(settings, "OPENAI_API_KEY", None)
        if not self.api_key:
            raise ValueError(
                "OPENAI_API_KEY not found. Please configure it via environment variables or pass it directly."
            )
        self.model = model

        from openai import OpenAI

        self.client = OpenAI(api_key=self.api_key)

    def get_chat_response(self, user_message: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": user_message}],
        )
        return response.choices[0].message.content

    def get_provider_name(self) -> AIProvider:
        return AIProvider.OPENAI
