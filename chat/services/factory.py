from django.conf import settings

from .base_service import BaseAIService
from .claude_service import ClaudeService
from .gemini_service import GeminiService
from .grok_service import GrokService
from .openai_service import OpenAIService
from .perplexity_service import PerplexityService


class AIServiceFactory:
    """
    Factory class for creating AI service instances based on configuration.

    This factory allows creating different AI service objects (Gemini, OpenAI, Claude,
    Perplexity, Grok) based on configuration, with all implementation details
    managed internally.
    """

    # Registry of available AI service providers
    _services: dict[str, type[BaseAIService]] = {
        "gemini": GeminiService,
        "openai": OpenAIService,
        "claude": ClaudeService,
        "perplexity": PerplexityService,
        "grok": GrokService,
    }

    @classmethod
    def create_service(cls, provider: str = None, api_key: str = None) -> BaseAIService:
        """
        Create an AI service instance based on the provider configuration.

        Args:
            provider: The AI provider name (gemini, openai, claude, perplexity, grok).
                     If not provided, uses settings.AI_PROVIDER or defaults to 'gemini'.
            api_key: Optional API key to use. If not provided, the service will use
                    the appropriate key from settings.

        Returns:
            An instance of the requested AI service

        Raises:
            ValueError: If the provider is not supported

        Examples:
            # Create using default provider from settings
            service = AIServiceFactory.create_service()

            # Create specific provider
            service = AIServiceFactory.create_service(provider='openai')

            # Create with custom API key
            service = AIServiceFactory.create_service(provider='gemini', api_key='your-key')
        """
        # Determine which provider to use
        if provider is None:
            provider = getattr(settings, "AI_PROVIDER", "gemini")

        provider = provider.lower()

        # Validate provider
        if provider not in cls._services:
            available = ", ".join(cls._services.keys())
            raise ValueError(
                f"Unsupported AI provider: '{provider}'. "
                f"Available providers: {available}"
            )

        # Create and return the service instance
        service_class = cls._services[provider]
        return service_class(api_key=api_key)

    @classmethod
    def get_available_providers(cls) -> list:
        """
        Get a list of all available AI providers.

        Returns:
            List of provider names
        """
        return list(cls._services.keys())

    @classmethod
    def register_provider(cls, name: str, service_class: type[BaseAIService]):
        """
        Register a new AI service provider.

        This allows extending the factory with custom AI service implementations.

        Args:
            name: The provider name (used in configuration)
            service_class: The service class that implements BaseAIService

        Raises:
            TypeError: If service_class doesn't inherit from BaseAIService
        """
        if not issubclass(service_class, BaseAIService):
            raise TypeError(f"{service_class.__name__} must inherit from BaseAIService")
        cls._services[name.lower()] = service_class
