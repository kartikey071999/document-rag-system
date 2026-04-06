from unittest.mock import Mock, patch

import pytest
from django.conf import settings

from app.providers import AIProvider, AIServiceFactory, BaseAIService, GeminiService


class TestAIServiceFactory:
    def test_factory_creates_default_service(self):
        with patch.object(settings, "AI_PROVIDER", AIProvider.GEMINI):
            with patch.object(settings, "GEMINI_API_KEY", "test-key"):
                with patch("app.providers.gemini.genai.Client"):
                    service = AIServiceFactory.create_service()
                    assert isinstance(service, GeminiService)

    def test_factory_creates_specific_provider(self):
        with patch.object(settings, "GEMINI_API_KEY", "test-key"):
            with patch("app.providers.gemini.genai.Client"):
                service = AIServiceFactory.create_service(provider=AIProvider.GEMINI)
                assert isinstance(service, GeminiService)
                assert service.get_provider_name() == AIProvider.GEMINI

    def test_factory_raises_on_invalid_provider(self):
        with pytest.raises(ValueError) as exc_info:
            AIServiceFactory.create_service(provider="invalid")
        assert "Unsupported AI provider" in str(exc_info.value)

    def test_factory_get_available_providers(self):
        providers = AIServiceFactory.get_available_providers()
        assert AIProvider.GEMINI in providers
        assert AIProvider.OPENAI in providers
        assert AIProvider.CLAUDE in providers
        assert AIProvider.PERPLEXITY in providers
        assert AIProvider.GROK in providers

    def test_factory_register_custom_provider(self):

        class CustomService(BaseAIService):
            def get_chat_response(self, user_message: str) -> str:
                return "custom response"

            def get_provider_name(self) -> str:
                return "Custom"

        AIServiceFactory.register_provider("custom", CustomService)
        assert "custom" in AIServiceFactory.get_available_providers()


class TestGeminiService:
    def test_service_initialization_without_api_key(self):
        with patch.object(settings, "GEMINI_API_KEY", ""):
            with pytest.raises(ValueError) as exc_info:
                GeminiService()
            assert "GEMINI_API_KEY not found" in str(exc_info.value)

    @patch("app.providers.gemini.genai.Client")
    def test_service_initialization_with_api_key(self, mock_client):
        with patch.object(settings, "GEMINI_API_KEY", "test-key"):
            GeminiService()
            mock_client.assert_called_once_with(api_key="test-key")

    @patch("app.providers.gemini.genai.Client")
    def test_get_chat_response(self, mock_client):
        mock_response = Mock()
        mock_response.text = "Hello! How can I help you?"
        mock_client_instance = Mock()
        mock_client_instance.models.generate_content.return_value = mock_response
        mock_client.return_value = mock_client_instance

        with patch.object(settings, "GEMINI_API_KEY", "test-key"):
            service = GeminiService()
            response = service.get_chat_response("Hello")

            assert response == "Hello! How can I help you?"
            mock_client_instance.models.generate_content.assert_called_once()

    @patch("app.providers.gemini.genai.Client")
    def test_get_provider_name(self, mock_client):
        with patch.object(settings, "GEMINI_API_KEY", "test-key"):
            service = GeminiService()
            assert service.get_provider_name() == AIProvider.GEMINI
