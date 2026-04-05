from __future__ import annotations

from typing import TYPE_CHECKING

from django.conf import settings

from .base import BaseAIService
from .enums import AIProvider, PerplexityModel

if TYPE_CHECKING:
    from openai import OpenAI


class PerplexityService(BaseAIService):

    def __init__(self, api_key: str = None, model: PerplexityModel = PerplexityModel.SONAR_SMALL):
        self.api_key = api_key or getattr(settings, "PERPLEXITY_API_KEY", None)
        if not self.api_key:
            raise ValueError(
                "PERPLEXITY_API_KEY not found. Please configure it via environment variables or pass it directly."
            )
        self.model = model

        from openai import OpenAI

        self.client = OpenAI(
            api_key=self.api_key, base_url="https://api.perplexity.ai"
        )

    def get_chat_response(self, user_message: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": user_message}],
        )
        return response.choices[0].message.content

    def get_provider_name(self) -> AIProvider:
        return AIProvider.PERPLEXITY
