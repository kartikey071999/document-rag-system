from .base import BaseAIService
from .enums import AIProvider, PerplexityModel


class PerplexityService(BaseAIService):
    def __init__(self, model: PerplexityModel = PerplexityModel.SONAR_SMALL):
        # TODO: Uncomment when API credits are available
        # if not getattr(settings, "PERPLEXITY_API_KEY", None):
        #     raise ValueError(
        #         "PERPLEXITY_API_KEY not found. Please configure it via environment variables."
        #     )
        self.model = model
        # self.client = OpenAI(
        #     api_key=settings.PERPLEXITY_API_KEY, base_url="https://api.perplexity.ai"
        # )

    def get_chat_response(
        self, user_message: str, system_prompt: str = None, filename: str = None
    ) -> str:
        # TODO: Uncomment when API credits are available
        # messages = []
        # if system_prompt:
        #     messages.append({"role": "system", "content": system_prompt})
        # content = user_message
        # if filename:
        #     content = f"[File: {filename}]\n\n{content}"
        # messages.append({"role": "user", "content": content})
        # response = self.client.chat.completions.create(
        #     model=self.model,
        #     messages=messages,
        # )
        # return response.choices[0].message.content

        # Mock response - remove this block when uncommenting above
        prompt = (
            f"[System: {system_prompt}]\n\n{user_message}"
            if system_prompt
            else user_message
        )
        file_info = f" | File: {filename}" if filename else ""
        return f"[MOCK {AIProvider.PERPLEXITY} | {self.model}{file_info}] {prompt}"

    def get_provider_name(self) -> AIProvider:
        return AIProvider.PERPLEXITY
