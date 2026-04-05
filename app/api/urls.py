from django.urls import path

from .routes import chat

app_name = "chat"

urlpatterns = [
    path("", chat.chat_view, name="chat"),
    path("send/", chat.send_message, name="send_message"),
    path("providers/", chat.get_providers, name="providers"),
]
