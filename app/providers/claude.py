from anthropic import Anthropic
from django.conf import settings

from .base import BaseAIService
from .enums import AIProvider, ClaudeModel


class ClaudeService(BaseAIService):

    def __init__(self, model: ClaudeModel = ClaudeModel.SONNET_3_5):
        if not getattr(settings, "ANTHROPIC_API_KEY", None):
            raise ValueError(
                "ANTHROPIC_API_KEY not found. Please configure it via environment variables."
            )
        self.model = model
        self.client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)

    def get_chat_response(self, user_message: str, system_prompt: str = None) -> str:
        kwargs = {
            "model": self.model,
            "max_tokens": 1024,
            "messages": [{"role": "user", "content": user_message}],
        }
        if system_prompt:
            kwargs["system"] = system_prompt
        response = self.client.messages.create(**kwargs)
        return response.content[0].text

    def get_provider_name(self) -> AIProvider:
        return AIProvider.CLAUDE
