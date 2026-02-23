from abc import ABC, abstractmethod


class BaseAIService(ABC):
    """Abstract base class for AI service providers."""

    @abstractmethod
    def get_chat_response(self, user_message: str) -> str:
        """
        Get a response from the AI provider for the given user message.

        Args:
            user_message: The message from the user

        Returns:
            The AI's response as a string

        Raises:
            Exception: If the API call fails
        """
        pass

    @abstractmethod
    def get_provider_name(self) -> str:
        """
        Get the name of the AI provider.

        Returns:
            The provider name as a string
        """
        pass
