from unittest.mock import Mock, patch

import pytest
from django.conf import settings

from chat.services import AIServiceFactory, BaseAIService, GeminiService


class TestAIServiceFactory:
    """Tests for AIServiceFactory."""

    def test_factory_creates_default_service(self):
        """Test that factory creates default service from settings."""
        with patch.object(settings, "AI_PROVIDER", "gemini"):
            with patch.object(settings, "GEMINI_API_KEY", "test-key"):
                with patch("chat.services.gemini_service.genai.Client"):
                    service = AIServiceFactory.create_service()
                    assert isinstance(service, GeminiService)

    def test_factory_creates_specific_provider(self):
        """Test that factory creates specific provider."""
        with patch.object(settings, "GEMINI_API_KEY", "test-key"):
            with patch("chat.services.gemini_service.genai.Client"):
                service = AIServiceFactory.create_service(provider="gemini")
                assert isinstance(service, GeminiService)
                assert service.get_provider_name() == "Gemini"

    def test_factory_raises_on_invalid_provider(self):
        """Test that factory raises error for invalid provider."""
        with pytest.raises(ValueError) as exc_info:
            AIServiceFactory.create_service(provider="invalid")
        assert "Unsupported AI provider" in str(exc_info.value)

    def test_factory_get_available_providers(self):
        """Test that factory returns list of available providers."""
        providers = AIServiceFactory.get_available_providers()
        assert "gemini" in providers
        assert "openai" in providers
        assert "claude" in providers
        assert "perplexity" in providers
        assert "grok" in providers

    def test_factory_register_custom_provider(self):
        """Test that factory can register custom provider."""

        class CustomService(BaseAIService):
            def get_chat_response(self, user_message: str) -> str:
                return "custom response"

            def get_provider_name(self) -> str:
                return "Custom"

        AIServiceFactory.register_provider("custom", CustomService)
        assert "custom" in AIServiceFactory.get_available_providers()


class TestGeminiService:
    """Tests for GeminiService."""

    def test_service_initialization_without_api_key(self):
        """Test that service raises error without API key."""
        with patch.object(settings, "GEMINI_API_KEY", ""):
            with pytest.raises(ValueError) as exc_info:
                GeminiService()
            assert "GEMINI_API_KEY not found" in str(exc_info.value)

    @patch("chat.services.gemini_service.genai.Client")
    def test_service_initialization_with_api_key(self, mock_client):
        """Test that service initializes with valid API key."""
        with patch.object(settings, "GEMINI_API_KEY", "test-key"):
            GeminiService()
            mock_client.assert_called_once_with(api_key="test-key")

    @patch("chat.services.gemini_service.genai.Client")
    def test_get_chat_response(self, mock_client):
        """Test that get_chat_response returns AI response."""
        # Setup mock
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

    @patch("chat.services.gemini_service.genai.Client")
    def test_get_provider_name(self, mock_client):
        """Test that get_provider_name returns correct name."""
        with patch.object(settings, "GEMINI_API_KEY", "test-key"):
            service = GeminiService()
            assert service.get_provider_name() == "Gemini"
