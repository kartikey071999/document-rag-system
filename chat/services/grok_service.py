from django.conf import settings

from .base_service import BaseAIService


class GrokService(BaseAIService):
    """Service class for interacting with xAI's Grok API."""

    def __init__(self, api_key: str = None):
        """
        Initialize the Grok service with API key.

        Args:
            api_key: Optional API key. If not provided, will use settings.XAI_API_KEY
        """
        self.api_key = api_key or getattr(settings, "XAI_API_KEY", None)
        if not self.api_key:
            raise ValueError(
                "XAI_API_KEY not found. Please configure it via environment variables or pass it directly."
            )

        try:
            from openai import OpenAI

            # Grok uses OpenAI-compatible API
            self.client = OpenAI(api_key=self.api_key, base_url="https://api.x.ai/v1")
        except ImportError as e:
            raise ImportError(
                "OpenAI package not installed. Install it with: pip install openai"
            ) from e

    def get_chat_response(self, user_message: str) -> str:
        """
        Get a response from Grok API for the given user message.

        Args:
            user_message: The message from the user

        Returns:
            The AI's response as a string

        Raises:
            Exception: If the API call fails
        """
        response = self.client.chat.completions.create(
            model="grok-beta",
            messages=[{"role": "user", "content": user_message}],
        )
        return response.choices[0].message.content

    def get_provider_name(self) -> str:
        """Get the provider name."""
        return "Grok"
