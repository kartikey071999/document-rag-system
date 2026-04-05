from django.conf import settings

from .base import BaseAIService


class GrokService(BaseAIService):

    def __init__(self, api_key: str = None):
        self.api_key = api_key or getattr(settings, "XAI_API_KEY", None)
        if not self.api_key:
            raise ValueError(
                "XAI_API_KEY not found. Please configure it via environment variables or pass it directly."
            )

        try:
            from openai import OpenAI

            self.client = OpenAI(api_key=self.api_key, base_url="https://api.x.ai/v1")
        except ImportError as e:
            raise ImportError(
                "OpenAI package not installed. Install it with: pip install openai"
            ) from e

    def get_chat_response(self, user_message: str) -> str:
        response = self.client.chat.completions.create(
            model="grok-beta",
            messages=[{"role": "user", "content": user_message}],
        )
        return response.choices[0].message.content

    def get_provider_name(self) -> str:
        return "Grok"
