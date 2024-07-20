import pytest
from rest_framework import status
from rest_framework.test import APIClient

from django.urls import reverse
from django.contrib.auth.models import User


@pytest.mark.django_db
class TestUserRegistrationView:
    """Test UserRegistrationView and depended serializer."""

    @pytest.fixture
    def client(self) -> APIClient:
        return APIClient()

    @pytest.fixture
    def url(self) -> str:
        return reverse("user-register")

    def test_user_registration_success(self, client: APIClient, url: str):
        """Test user registration success."""
        data = {
            "username": "newuser",
            "password": "securepassword123",
            "password_confirm": "securepassword123",
        }
        response = client.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["username"] == "newuser"
        assert User.objects.filter(username=data["username"]).exists()

    def test_user_registration_password_mismatch(
        self, client: APIClient, url: str
    ):
        """Test user registration password mismatch."""
        data = {
            "username": "newuser",
            "password": "securepassword123",
            "password_confirm": "differentpassword",
        }
        response = client.post(url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "password_confirm" in response.data
        assert (
            str(response.data["password_confirm"][0]) == "Passwords must match"
        )
        assert not User.objects.filter(username=data["username"]).exists()
