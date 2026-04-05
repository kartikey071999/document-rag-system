from app.providers import AIServiceFactory


class ChatService:

    def __init__(self):
        self.ai_service = AIServiceFactory.create_service()

    def send_message(self, user_message: str) -> dict:
        ai_response = self.ai_service.get_chat_response(user_message)
        return {
            "user_message": user_message,
            "ai_response": ai_response,
            "provider": self.ai_service.get_provider_name(),
        }