from app.providers import AIServiceFactory


class ChatService:

    def __init__(self, provider: str = None, model: str = None):
        self.ai_service = AIServiceFactory.create_service(provider=provider, model=model)

    def send_message(self, user_message: str, system_prompt: str = None) -> dict:
        ai_response = self.ai_service.get_chat_response(user_message, system_prompt=system_prompt)
        return {
            "user_message": user_message,
            "ai_response": ai_response,
            "provider": self.ai_service.get_provider_name(),
        }