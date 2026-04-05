import pytest
from django.test import Client
from django.urls import reverse


@pytest.fixture
def client():
    return Client()


@pytest.mark.django_db
class TestChatViews:

    def test_chat_view_loads(self, client):
        response = client.get(reverse("chat:chat"))
        assert response.status_code == 200
        assert b"AI Chat Assistant" in response.content

    def test_send_message_requires_post(self, client):
        response = client.get(reverse("chat:send_message"))
        assert response.status_code == 405  # Method not allowed

    def test_send_message_empty_message(self, client):
        response = client.post(reverse("chat:send_message"), {"message": ""})
        assert response.status_code == 400
        data = response.json()
        assert "error" in data
