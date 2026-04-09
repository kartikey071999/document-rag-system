from enum import StrEnum


class AIProvider(StrEnum):
    GEMINI = "gemini"
    OPENAI = "openai"
    CLAUDE = "claude"
    PERPLEXITY = "perplexity"
    GROK = "grok"
    NVIDIA = "nvidia"
    GROQ = "groq"


class ModelCapability(StrEnum):
    CHAT = "chat"
    TRANSCRIPTION = "transcription"
    TTS = "text-to-speech"


class GeminiModel(StrEnum):
    FLASH_2 = "gemini-2.0-flash"
    FLASH_2_LITE = "gemini-2.0-flash-lite"
    FLASH_1_5 = "gemini-1.5-flash"
    PRO_2_5 = "gemini-2.5-pro-preview-05-06"
    FLASH_3 = "gemini-3-flash-preview"


class OpenAIModel(StrEnum):
    GPT_4O = "gpt-4o"
    GPT_4O_MINI = "gpt-4o-mini"
    GPT_4_TURBO = "gpt-4-turbo"
    O3_MINI = "o3-mini"


class ClaudeModel(StrEnum):
    SONNET_3_5 = "claude-3-5-sonnet-20241022"
    SONNET_4 = "claude-sonnet-4-20250514"
    HAIKU_3_5 = "claude-3-5-haiku-20241022"
    OPUS_4 = "claude-opus-4-20250514"


class GrokModel(StrEnum):
    GROK_BETA = "grok-beta"
    GROK_3 = "grok-3"
    GROK_3_MINI = "grok-3-mini"


class PerplexityModel(StrEnum):
    SONAR_SMALL = "llama-3.1-sonar-small-128k-online"
    SONAR_LARGE = "llama-3.1-sonar-large-128k-online"
    SONAR_HUGE = "llama-3.1-sonar-huge-128k-online"


class NvidiaModel(StrEnum):
    NEMOTRON_3_NANO = "nvidia/nemotron-3-nano-30b-a3b"


class GroqChatModel(StrEnum):
    LLAMA_3_3_70B = "llama-3.3-70b-versatile"
    LLAMA_3_1_8B = "llama-3.1-8b-instant"
    LLAMA_4_SCOUT = "meta-llama/llama-4-scout-17b-16e-instruct"
    QWEN3_32B = "qwen/qwen3-32b"
    KIMI_K2 = "moonshotai/kimi-k2-instruct"
    KIMI_K2_0905 = "moonshotai/kimi-k2-instruct-0905"
    COMPOUND = "groq/compound"
    COMPOUND_MINI = "groq/compound-mini"
    GPT_OSS_120B = "openai/gpt-oss-120b"
    GPT_OSS_20B = "openai/gpt-oss-20b"
    ALLAM_2_7B = "allam-2-7b"


class GroqTranscriptionModel(StrEnum):
    WHISPER_LARGE_V3 = "whisper-large-v3"
    WHISPER_LARGE_V3_TURBO = "whisper-large-v3-turbo"


class GroqTTSModel(StrEnum):
    ORPHEUS_ENGLISH = "canopylabs/orpheus-v1-english"
    ORPHEUS_ARABIC_SAUDI = "canopylabs/orpheus-arabic-saudi"


class GroqGuardModel(StrEnum):
    PROMPT_GUARD_22M = "meta-llama/llama-prompt-guard-2-22m"
    PROMPT_GUARD_86M = "meta-llama/llama-prompt-guard-2-86m"
    SAFEGUARD_20B = "openai/gpt-oss-safeguard-20b"


PROVIDER_MODELS: dict[AIProvider, type[StrEnum]] = {
    AIProvider.GEMINI: GeminiModel,
    AIProvider.OPENAI: OpenAIModel,
    AIProvider.CLAUDE: ClaudeModel,
    AIProvider.GROK: GrokModel,
    AIProvider.PERPLEXITY: PerplexityModel,
    AIProvider.NVIDIA: NvidiaModel,
    AIProvider.GROQ: GroqChatModel,
}
