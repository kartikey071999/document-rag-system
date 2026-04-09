from django.conf import settings
from openai import OpenAI

from .base import BaseAIService
from .enums import AIProvider, NvidiaModel


class NvidiaService(BaseAIService):
    def __init__(self, model: NvidiaModel = NvidiaModel.NEMOTRON_3_NANO):
        self.model = model
        api_key = getattr(settings, "NVIDIA_API_KEY", None)
        if not api_key:
            raise ValueError(
                "NVIDIA_API_KEY not found. Please configure it via environment variables."
            )
        self.client = OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=api_key,
        )

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
            temperature=1,
            top_p=1,
            max_tokens=16384,
            extra_body={
                "reasoning_budget": 16384,
                "chat_template_kwargs": {"enable_thinking": True},
            },
            stream=True,
        )

        reasoning_text = ""
        response_text = ""
        for chunk in completion:
            if not chunk.choices:
                continue
            reasoning = getattr(chunk.choices[0].delta, "reasoning_content", None)
            if reasoning:
                reasoning_text += reasoning
            if chunk.choices[0].delta.content is not None:
                response_text += chunk.choices[0].delta.content

        return response_text

    def get_provider_name(self) -> AIProvider:
        return AIProvider.NVIDIA
