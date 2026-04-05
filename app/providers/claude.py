from django.conf import settings

from .base import BaseAIService


class ClaudeService(BaseAIService):

    def __init__(self, api_key: str = None):
        self.api_key = api_key or getattr(settings, "ANTHROPIC_API_KEY", None)
        if not self.api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY not found. Please configure it via environment variables or pass it directly."
            )

        try:
            from anthropic import Anthropic

            self.client = Anthropic(api_key=self.api_key)
        except ImportError as e:
            raise ImportError(
                "Anthropic package not installed. Install it with: pip install anthropic"
            ) from e

    def get_chat_response(self, user_message: str) -> str:
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[{"role": "user", "content": user_message}],
        )
        return response.content[0].text

    def get_provider_name(self) -> str:
        return "Claude"
