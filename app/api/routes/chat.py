from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from app.api.services.chat import ChatService


def chat_view(request):
    return render(request, "chat/chat.html")


@require_http_methods(["POST"])
def send_message(request):
    """Handle chat message submission and return AI response as JSON."""
    user_message = request.POST.get("message", "").strip()

    if not user_message:
        return JsonResponse({"error": "Message cannot be empty"}, status=400)

    try:
        chat_service = ChatService()
        result = chat_service.send_message(user_message)
        return JsonResponse(result)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
