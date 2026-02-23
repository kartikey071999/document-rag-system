from django.conf import settings
from google import genai

from .base_service import BaseAIService


class GeminiService(BaseAIService):
    """Service class for interacting with Google's Gemini API."""

    def __init__(self, api_key: str = None):
        """
        Initialize the Gemini service with API key.

        Args:
            api_key: Optional API key. If not provided, will use settings.GEMINI_API_KEY
        """
        self.api_key = api_key or settings.GEMINI_API_KEY
        if not self.api_key:
            raise ValueError(
                "GEMINI_API_KEY not found. Please configure it via environment variables or pass it directly."
            )
        self.client = genai.Client(api_key=self.api_key)

    def get_chat_response(self, user_message: str) -> str:
        """
        Get a response from Gemini API for the given user message.

        Args:
            user_message: The message from the user

        Returns:
            The AI's response as a string

        Raises:
            Exception: If the API call fails
        """
        response = self.client.models.generate_content(
            model="gemini-3-flash-preview", contents=user_message
        )
        return response.text

    def get_provider_name(self) -> str:
        """Get the provider name."""
        return "Gemini"
