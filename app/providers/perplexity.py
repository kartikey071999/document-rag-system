from django.conf import settings

from .base import BaseAIService


class PerplexityService(BaseAIService):

    def __init__(self, api_key: str = None):
        self.api_key = api_key or getattr(settings, "PERPLEXITY_API_KEY", None)
        if not self.api_key:
            raise ValueError(
                "PERPLEXITY_API_KEY not found. Please configure it via environment variables or pass it directly."
            )

        try:
            from openai import OpenAI

            self.client = OpenAI(
                api_key=self.api_key, base_url="https://api.perplexity.ai"
            )
        except ImportError as e:
            raise ImportError(
                "OpenAI package not installed. Install it with: pip install openai"
            ) from e

    def get_chat_response(self, user_message: str) -> str:
        response = self.client.chat.completions.create(
            model="llama-3.1-sonar-small-128k-online",
            messages=[{"role": "user", "content": user_message}],
        )
        return response.choices[0].message.content

    def get_provider_name(self) -> str:
        return "Perplexity"
