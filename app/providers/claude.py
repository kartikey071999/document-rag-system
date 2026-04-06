from .base import BaseAIService
from .enums import AIProvider, ClaudeModel


class ClaudeService(BaseAIService):
    def __init__(self, model: ClaudeModel = ClaudeModel.SONNET_3_5):
        # TODO: Uncomment when API credits are available
        # if not getattr(settings, "ANTHROPIC_API_KEY", None):
        #     raise ValueError(
        #         "ANTHROPIC_API_KEY not found. Please configure it via environment variables."
        #     )
        self.model = model
        # self.client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)

    def get_chat_response(
        self, user_message: str, system_prompt: str = None, filename: str = None
    ) -> str:
        # TODO: Uncomment when API credits are available
        # message_content = user_message
        # if filename:
        #     message_content = f"[File: {filename}]\n\n{message_content}"
        # kwargs = {
        #     "model": self.model,
        #     "max_tokens": 1024,
        #     "messages": [{"role": "user", "content": message_content}],
        # }
        # if system_prompt:
        #     kwargs["system"] = system_prompt
        # response = self.client.messages.create(**kwargs)
        # return response.content[0].text

        # Mock response - remove this block when uncommenting above
        prompt = (
            f"[System: {system_prompt}]\n\n{user_message}"
            if system_prompt
            else user_message
        )
        file_info = f" | File: {filename}" if filename else ""
        return f"[MOCK {AIProvider.CLAUDE} | {self.model}{file_info}] {prompt}"

    def get_provider_name(self) -> AIProvider:
        return AIProvider.CLAUDE
