from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from app.api.services.chat import ChatService
from app.providers.enums import PROVIDER_MODELS, AIProvider


def chat_view(request):
    return render(request, "chat/chat.html")


@require_http_methods(["POST"])
def send_message(request):
    """Handle chat message submission and return AI response as JSON."""
    user_message = request.POST.get("message", "").strip()
    provider = request.POST.get("provider", "").strip() or None
    model = request.POST.get("model", "").strip() or None
    system_prompt = request.POST.get("system_prompt", "").strip() or None

    if not user_message:
        return JsonResponse({"error": "Message cannot be empty"}, status=400)

    try:
        chat_service = ChatService(provider=provider, model=model)
        result = chat_service.send_message(user_message, system_prompt=system_prompt)
        return JsonResponse(result)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@require_http_methods(["GET"])
def get_providers(request):
    """Return available providers and their models."""
    data = {}
    for provider, model_enum in PROVIDER_MODELS.items():
        data[provider.value] = {
            "models": [{"value": m.value, "name": m.name} for m in model_enum],
            "default": list(model_enum)[0].value,
        }
    return JsonResponse(data)
