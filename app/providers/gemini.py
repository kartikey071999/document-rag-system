from .base import BaseAIService
from .enums import AIProvider, GeminiModel


class GeminiService(BaseAIService):
    def __init__(self, model: GeminiModel = GeminiModel.FLASH_3):
        # TODO: Uncomment when API credits are available
        # if not settings.GEMINI_API_KEY:
        #     raise ValueError(
        #         "GEMINI_API_KEY not found. Please configure it via environment variables."
        #     )
        self.model = model
        # self.client = genai.Client(api_key=settings.GEMINI_API_KEY)

    def get_chat_response(
        self, user_message: str, system_prompt: str = None, filename: str = None
    ) -> str:
        # TODO: Uncomment when API credits are available
        # contents = user_message
        # if filename:
        #     contents = f"[File: {filename}]\n\n{contents}"
        # if system_prompt:
        #     contents = f"{system_prompt}\n\n{contents}"
        # response = self.client.models.generate_content(
        #     model=self.model, contents=contents
        # )
        # return response.text

        # Mock response - remove this block when uncommenting above
        prompt = (
            f"[System: {system_prompt}]\n\n{user_message}"
            if system_prompt
            else user_message
        )
        file_info = f" | File: {filename}" if filename else ""
        return f"[MOCK {AIProvider.GEMINI} | {self.model}{file_info}] {prompt}"

    def get_provider_name(self) -> AIProvider:
        return AIProvider.GEMINI
