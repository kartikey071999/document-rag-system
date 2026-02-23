# AI Service Factory Pattern

This document explains the AI service factory pattern implementation in the document RAG system.

## Overview

The project uses a **Factory Pattern** to support multiple AI providers (Gemini, OpenAI, Claude, Perplexity, Grok) with a unified interface. This design allows easy switching between providers through configuration without changing application code.

## Architecture

```
chat/services/
├── base_service.py          # Abstract base class defining the interface
├── factory.py               # Factory class for creating AI service instances
├── gemini_service.py        # Google Gemini implementation
├── openai_service.py        # OpenAI implementation  
├── claude_service.py        # Anthropic Claude implementation
├── perplexity_service.py    # Perplexity AI implementation
└── grok_service.py          # xAI Grok implementation
```

## Usage

### Basic Usage

```python
from chat.services import AIServiceFactory

# Create service using default provider from settings
service = AIServiceFactory.create_service()
response = service.get_chat_response("Hello, AI!")
```

### Specify Provider

```python
# Create specific provider
gemini_service = AIServiceFactory.create_service(provider='gemini')
openai_service = AIServiceFactory.create_service(provider='openai')
claude_service = AIServiceFactory.create_service(provider='claude')
```

### Custom API Key

```python
# Use custom API key instead of settings
service = AIServiceFactory.create_service(
    provider='gemini',
    api_key='your-custom-api-key'
)
```

## Configuration

Set the AI provider in your `.env` file:

```bash
# Choose your AI provider
AI_PROVIDER=gemini  # Options: gemini, openai, claude, perplexity, grok

# Add the corresponding API key
GEMINI_API_KEY=your-key-here
OPENAI_API_KEY=your-key-here
ANTHROPIC_API_KEY=your-key-here
PERPLEXITY_API_KEY=your-key-here
XAI_API_KEY=your-key-here
```

## Supported Providers

| Provider | Package Required | Model Used |
|----------|-----------------|------------|
| Gemini | `google-genai` | gemini-2.0-flash-exp |
| OpenAI | `openai` | gpt-4o-mini |
| Claude | `anthropic` | claude-3-5-sonnet-20241022 |
| Perplexity | `openai` | llama-3.1-sonar-small-128k-online |
| Grok | `openai` | grok-beta |

## Installing Provider Dependencies

### Gemini (Default)
```bash
pip install google-genai
```

### OpenAI, Perplexity, Grok
```bash
pip install openai
```

### Claude
```bash
pip install anthropic
```

## Extending with Custom Providers

You can register custom AI providers:

```python
from chat.services import AIServiceFactory, BaseAIService

class MyCustomAI(BaseAIService):
    def __init__(self, api_key: str = None):
        self.api_key = api_key or settings.CUSTOM_API_KEY
        # Initialize your client
    
    def get_chat_response(self, user_message: str) -> str:
        # Implement your AI logic
        return "Custom AI response"
    
    def get_provider_name(self) -> str:
        return "CustomAI"

# Register the custom provider
AIServiceFactory.register_provider('custom', MyCustomAI)

# Use it
service = AIServiceFactory.create_service(provider='custom')
```

## Benefits

1. **Flexibility**: Switch AI providers without code changes
2. **Extensibility**: Easy to add new providers
3. **Consistency**: All providers follow the same interface
4. **Testability**: Easy to mock and test
5. **Configuration-driven**: Provider selection via environment variables

## Implementation Details

### Base Service Interface

All AI services implement the `BaseAIService` abstract class:

```python
class BaseAIService(ABC):
    @abstractmethod
    def get_chat_response(self, user_message: str) -> str:
        """Get AI response for user message"""
        pass
    
    @abstractmethod
    def get_provider_name(self) -> str:
        """Return provider name"""
        pass
```

### Factory Method

The factory creates instances based on configuration:

```python
service = AIServiceFactory.create_service(
    provider=None,  # Uses settings.AI_PROVIDER if not specified
    api_key=None    # Uses provider-specific key from settings if not specified
)
```

## Error Handling

The factory provides clear error messages:

- **Missing API Key**: Raised when required API key is not configured
- **Unsupported Provider**: Raised when invalid provider name is used
- **Missing Package**: Raised when required SDK is not installed

## Testing

Tests are provided in `chat/test_services.py`:

```bash
# Run all service tests
pytest chat/test_services.py -v

# Run specific test
pytest chat/test_services.py::TestAIServiceFactory -v
```
