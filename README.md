# Document RAG System

A Django web application with an AI chat interface supporting multiple AI providers (Gemini, OpenAI, Claude, Perplexity, Grok) through a factory pattern. Features clean, modular architecture designed for future Retrieval-Augmented Generation (RAG) system integration.

## Features

- 🤖 **Multi-Provider AI Support**: Gemini, OpenAI, Claude, Perplexity, Grok via factory pattern
- 🏭 **Factory Pattern**: Switch AI providers through configuration, no code changes needed
- 🎨 Clean and modern UI with responsive design
- 🏗️ Modular architecture with separate service layer
- 🔐 Secure API key management using environment variables
- 📦 Ready for RAG system integration
- ✅ CI/CD pipeline with automated testing and linting
- 🧪 Comprehensive test coverage with pytest
- 🎯 Code quality enforced with ruff and black

## CI/CD Pipeline

The project includes a complete CI/CD setup with GitHub Actions:

- **Linting & Formatting**: Automated checks with `ruff` and `black`
- **Testing**: Runs on Python 3.11 and 3.12 with pytest
- **Structure Validation**: Ensures project structure integrity
- **Security Scanning**: Automated security checks with bandit and safety
- **Coverage Reports**: Test coverage tracking with codecov

## Architecture

The application follows a clean, modular structure:

```
document-rag-system/
├── config/                 # Django project settings
│   ├── settings.py        # Main settings with environment variable support
│   └── urls.py            # Root URL configuration
├── chat/                   # Chat application
│   ├── services/          # Service layer (business logic)
│   │   └── gemini_service.py  # Gemini API integration
│   ├── templates/chat/    # HTML templates
│   │   └── chat.html      # Chat interface
│   ├── views.py           # View handlers
│   └── urls.py            # App URL configuration
└── manage.py              # Django management script
```

### Key Design Principles

1. **Service Layer Separation**: AI logic is isolated in `chat/services/gemini_service.py`, keeping views clean and focused on HTTP handling.
2. **Environment-based Configuration**: API keys and sensitive settings are managed through environment variables.
3. **Modular Structure**: Each component has a single responsibility, making it easy to extend or modify.
4. **RAG-Ready Architecture**: The service layer design allows for easy integration of document retrieval and RAG capabilities.
