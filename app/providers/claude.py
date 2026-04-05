from django.conf import settings

from .base import BaseAIService


class ClaudeService(BaseAIService):
    """Service class for interacting with Anthropic's Claude API."""

    def __init__(self, api_key: str = None):
        """
        Initialize the Claude service with API key.

        Args:
            api_key: Optional API key. If not provided, will use settings.ANTHROPIC_API_KEY
        """
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
        """
        Get a response from Claude API for the given user message.

        Args:
            user_message: The message from the user

        Returns:
            The AI's response as a string

        Raises:
            Exception: If the API call fails
        """
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[{"role": "user", "content": user_message}],
        )
        return response.content[0].text

    def get_provider_name(self) -> str:
        """Get the provider name."""
        return "Claude"
