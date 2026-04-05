from __future__ import annotations

from typing import TYPE_CHECKING

from django.conf import settings

from .base import BaseAIService
from .enums import AIProvider, ClaudeModel

if TYPE_CHECKING:
    from anthropic import Anthropic


class ClaudeService(BaseAIService):

    def __init__(self, api_key: str = None, model: ClaudeModel = ClaudeModel.SONNET_3_5):
        self.api_key = api_key or getattr(settings, "ANTHROPIC_API_KEY", None)
        if not self.api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY not found. Please configure it via environment variables or pass it directly."
            )
        self.model = model

        from anthropic import Anthropic

        self.client = Anthropic(api_key=self.api_key)

    def get_chat_response(self, user_message: str) -> str:
        response = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=[{"role": "user", "content": user_message}],
        )
        return response.content[0].text

    def get_provider_name(self) -> AIProvider:
        return AIProvider.CLAUDE
