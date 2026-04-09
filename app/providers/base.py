from abc import ABC, abstractmethod


class BaseAIService(ABC):
    @abstractmethod
    def get_chat_response(
        self, user_message: str, system_prompt: str = None, filename: str = None
    ) -> str:
        pass

    @abstractmethod
    def get_provider_name(self):
        pass

    def get_capabilities(self) -> list[str]:
        return ["chat"]

    def get_transcription(self, audio_filepath: str, language: str = None) -> str:
        raise NotImplementedError(
            f"{self.get_provider_name()} does not support transcription."
        )

    def get_speech(self, text: str, voice: str = None) -> bytes:
        raise NotImplementedError(
            f"{self.get_provider_name()} does not support text-to-speech."
        )
