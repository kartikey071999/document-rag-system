from django.conf import settings

from .base import BaseAIService
from .claude import ClaudeService
from .gemini import GeminiService
from .grok import GrokService
from .openai import OpenAIService
from .perplexity import PerplexityService


class AIServiceFactory:

    _services: dict[str, type[BaseAIService]] = {
        "gemini": GeminiService,
        "openai": OpenAIService,
        "claude": ClaudeService,
        "perplexity": PerplexityService,
        "grok": GrokService,
    }

    @classmethod
    def create_service(cls, provider: str = None, api_key: str = None) -> BaseAIService:
        """Create and return an AI service instance for the given provider."""
        if provider is None:
            provider = getattr(settings, "AI_PROVIDER", "gemini")

        provider = provider.lower()

        if provider not in cls._services:
            available = ", ".join(cls._services.keys())
            raise ValueError(
                f"Unsupported AI provider: '{provider}'. "
                f"Available providers: {available}"
            )

        service_class = cls._services[provider]
        return service_class(api_key=api_key)

    @classmethod
    def get_available_providers(cls) -> list:
        """Return list of registered provider names."""
        return list(cls._services.keys())

    @classmethod
    def register_provider(cls, name: str, service_class: type[BaseAIService]):
        """Register a new AI service provider."""
        if not issubclass(service_class, BaseAIService):
            raise TypeError(f"{service_class.__name__} must inherit from BaseAIService")
        cls._services[name.lower()] = service_class
