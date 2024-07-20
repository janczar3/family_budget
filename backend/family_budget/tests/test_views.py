import pytest
from rest_framework import status
from rest_framework.test import APIClient

from django.urls import reverse
from django.contrib.auth.models import User


@pytest.mark.django_db
class TestUserViewSet:
    """Test UserViewSet and depended serializer."""

    @pytest.fixture
    def client(self) -> APIClient:
        return APIClient()

    @pytest.fixture
    def user(self):
        return User.objects.create_user(
            username="testuser", password="testpassword"
        )

    @pytest.fixture
    def register_url(self) -> str:
        return reverse("user-register")

    @pytest.fixture
    def login_url(self) -> str:
        return reverse("user-login")

    @pytest.fixture
    def logout_url(self) -> str:
        return reverse("user-logout")

    def test_user_registration_success(
        self, client: APIClient, register_url: str
    ):
        """Test user registration success."""
        data = {
            "username": "newuser",
            "password": "securepassword123",
            "password_confirm": "securepassword123",
        }
        response = client.post(register_url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.filter(username=data["username"]).exists()

    def test_user_registration_password_mismatch(
        self, client: APIClient, register_url: str
    ):
        """Test user registration password mismatch."""
        data = {
            "username": "newuser",
            "password": "securepassword123",
            "password_confirm": "differentpassword",
        }
        response = client.post(register_url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "password_confirm" in response.data
        assert (
            str(response.data["password_confirm"][0]) == "Passwords must match"
        )
        assert not User.objects.filter(username=data["username"]).exists()

    def test_login_success(self, client: APIClient, user: User, login_url: str):
        """Test login success."""
        data = {
            "username": "testuser",
            "password": "testpassword",
        }
        response = client.post(login_url, data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert "access_token" in response.data
        assert "access_token" in response.data

    def test_login_user_not_exists(self, client: APIClient, login_url: str):
        """Test login user not exists."""
        data = {
            "username": "wronguser",
            "password": "wrongpassword",
        }
        response = client.post(login_url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
