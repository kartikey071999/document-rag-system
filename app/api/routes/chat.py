from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from app.providers import AIServiceFactory


def chat_view(request):
    return render(request, "chat/chat.html")


@require_http_methods(["POST"])
def send_message(request):
    """Handle chat message submission and return AI response as JSON."""
    user_message = request.POST.get("message", "").strip()

    if not user_message:
        return JsonResponse({"error": "Message cannot be empty"}, status=400)

    try:
        ai_service = AIServiceFactory.create_service()
        ai_response = ai_service.get_chat_response(user_message)

        return JsonResponse(
            {
                "user_message": user_message,
                "ai_response": ai_response,
                "provider": ai_service.get_provider_name(),
            }
        )
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
