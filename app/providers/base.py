from abc import ABC, abstractmethod


class BaseAIService(ABC):

    @abstractmethod
    def get_chat_response(self, user_message: str) -> str:
        pass

    @abstractmethod
    def get_provider_name(self):
        pass
