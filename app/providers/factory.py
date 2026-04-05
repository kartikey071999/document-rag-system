from django.conf import settings

from .base import BaseAIService
from .claude import ClaudeService
from .enums import AIProvider
from .gemini import GeminiService
from .grok import GrokService
from .openai import OpenAIService
from .perplexity import PerplexityService


class AIServiceFactory:

    _services: dict[AIProvider, type[BaseAIService]] = {
        AIProvider.GEMINI: GeminiService,
        AIProvider.OPENAI: OpenAIService,
        AIProvider.CLAUDE: ClaudeService,
        AIProvider.PERPLEXITY: PerplexityService,
        AIProvider.GROK: GrokService,
    }

    @classmethod
    def create_service(cls, provider: AIProvider | str = None, model: str = None) -> BaseAIService:
        """Create and return an AI service instance for the given provider."""
        if provider is None:
            provider = getattr(settings, "AI_PROVIDER", AIProvider.GEMINI)

        if isinstance(provider, str):
            try:
                provider = AIProvider(provider.lower())
            except ValueError:
                provider = provider.lower()

        if provider not in cls._services:
            available = ", ".join(p.value for p in AIProvider)
            raise ValueError(
                f"Unsupported AI provider: '{provider}'. "
                f"Available providers: {available}"
            )

        service_class = cls._services[provider]
        kwargs = {}
        if model:
            kwargs["model"] = model
        return service_class(**kwargs)

    @classmethod
    def get_available_providers(cls) -> list[AIProvider]:
        """Return list of registered provider enums."""
        return list(cls._services.keys())

    @classmethod
    def register_provider(cls, name: AIProvider | str, service_class: type[BaseAIService]):
        """Register a new AI service provider."""
        if not issubclass(service_class, BaseAIService):
            raise TypeError(f"{service_class.__name__} must inherit from BaseAIService")
        if isinstance(name, str):
            try:
                name = AIProvider(name.lower())
            except ValueError:
                pass
        cls._services[name] = service_class
