from django.conf import settings
from groq import Groq

from .base import BaseAIService
from .enums import (
    AIProvider,
    GroqChatModel,
    GroqTranscriptionModel,
    GroqTTSModel,
)


class GroqService(BaseAIService):
    def __init__(self, model: GroqChatModel = GroqChatModel.LLAMA_3_3_70B):
        self.model = model
        api_key = getattr(settings, "GROQ_API_KEY", None)
        if not api_key:
            raise ValueError(
                "GROQ_API_KEY not found. Please configure it via environment variables."
            )
        self.client = Groq(api_key=api_key)

    def get_chat_response(
        self, user_message: str, system_prompt: str = None, filename: str = None
    ) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        content = user_message
        if filename:
            content = f"[File: {filename}]\n\n{content}"
        messages.append({"role": "user", "content": content})

        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
        )
        return completion.choices[0].message.content

    def get_transcription(
        self,
        audio_filepath: str,
        language: str = None,
        model: GroqTranscriptionModel = GroqTranscriptionModel.WHISPER_LARGE_V3_TURBO,
    ) -> str:
        with open(audio_filepath, "rb") as audio_file:
            kwargs = {
                "file": ("audio", audio_file),
                "model": model,
            }
            if language:
                kwargs["language"] = language
            transcription = self.client.audio.transcriptions.create(**kwargs)
        return transcription.text

    def get_speech(
        self,
        text: str,
        voice: str = None,
        model: GroqTTSModel = GroqTTSModel.ORPHEUS_ENGLISH,
    ) -> bytes:
        response = self.client.audio.speech.create(
            model=model,
            input=text,
            voice=voice or "orpheus-tara",
            response_format="wav",
        )
        return response.read()

    def get_capabilities(self) -> list[str]:
        return ["chat", "transcription", "text-to-speech"]

    def get_provider_name(self) -> AIProvider:
        return AIProvider.GROQ
