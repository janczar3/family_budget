import pytest
from rest_framework import status
from rest_framework.test import APIClient
from django_dynamic_fixture import G

from django.urls import reverse
from django.contrib.auth.models import User

from family_budget.models import Budget


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


@pytest.mark.django_db
class TestBudgetViewSet:
    """BudgetViewSet and depended serializer."""

    @pytest.fixture
    def user_owner(self) -> User:
        """User who owns the budget."""
        return User.objects.create_user(username="user", password="password")

    @pytest.fixture
    def user_member(self) -> User:
        """User who is member of the budget."""
        return User.objects.create_user(
            username="user_member", password="password"
        )

    @pytest.fixture
    def user_not_member(self) -> User:
        """User who is not member and not owner of the budget."""
        return User.objects.create_user(
            username="user_not_member", password="password"
        )

    @pytest.fixture
    def authenticated_client_owner(self, user_owner: User) -> APIClient:
        """Owner api client."""
        client = APIClient()
        client.force_authenticate(user=user_owner)
        return client

    @pytest.fixture
    def authenticated_client_member(self, user_member: User) -> APIClient:
        """Member api client."""
        client = APIClient()
        client.force_authenticate(user=user_member)
        return client

    @pytest.fixture
    def authenticated_client_not_member(
        self, user_not_member: User
    ) -> APIClient:
        """Not member api client."""
        client = APIClient()
        client.force_authenticate(user=user_not_member)
        return client

    @pytest.fixture
    def anonymous_client(self) -> APIClient:
        """Anonymous api client."""
        client = APIClient()
        return client

    @pytest.fixture
    def budget(self, user_owner: User, user_member: User) -> Budget:
        """Budget fixture."""
        return G(Budget, name="budget_1", owner=user_owner, users=[user_member])

    def test_create_budget(
        self, authenticated_client_owner: APIClient, user_owner: User
    ):
        """Test create budget."""
        data = {
            "name": "budget_1",
        }
        url = reverse("budget-list")
        response = authenticated_client_owner.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["name"] == data["name"]
        assert response.data["owner"] == user_owner.pk
        assert Budget.objects.filter(name=data["name"]).exists()

    def test_create_budget_anonymous(self, anonymous_client: APIClient):
        """Test create budget anonymous should fail."""
        data = {
            "name": "budget_1",
        }
        url = reverse("budget-list")
        response = anonymous_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert not Budget.objects.filter(name=data["name"]).exists()

    def test_update_budget(
        self,
        authenticated_client_owner: APIClient,
        user_owner: User,
        budget: Budget,
    ):
        """Test update budget."""
        data = {"name": "new_budget_name"}
        url = reverse("budget-detail", kwargs={"pk": budget.pk})
        response = authenticated_client_owner.patch(url, data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == data["name"]
        assert response.data["owner"] == user_owner.pk
        assert Budget.objects.filter(name=data["name"]).exists()

    def test_update_budget_anonymous(
        self, anonymous_client: APIClient, budget: Budget
    ):
        """Test update budget anonymous should fail."""
        data = {"name": "new_budget_name"}
        url = reverse("budget-detail", kwargs={"pk": budget.pk})
        response = anonymous_client.patch(url, data, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert not Budget.objects.filter(name=data["name"]).exists()

    def test_update_budget_user_is_not_owner(
        self, authenticated_client_member: APIClient, budget: Budget
    ):
        """Test update budget by member only should fail."""
        data = {"name": "new_budget_name"}
        url = reverse("budget-detail", kwargs={"pk": budget.pk})
        response = authenticated_client_member.patch(url, data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert not Budget.objects.filter(name=data["name"]).exists()

    def test_retrieve_budget_user_is_owner(
        self,
        authenticated_client_owner: APIClient,
        budget: Budget,
        user_owner: User,
        user_member: User,
    ):
        """Test retrieve budget by owner."""
        url = reverse("budget-detail", kwargs={"pk": budget.pk})
        response = authenticated_client_owner.get(url, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            "id": budget.pk,
            "name": budget.name,
            "owner": user_owner.pk,
            "users": [user_member.pk],
        }

    def test_retrieve_budget_user_is_member(
        self,
        authenticated_client_member: APIClient,
        budget: Budget,
        user_owner: User,
        user_member: User,
    ):
        """Test retrieve budget by member."""
        url = reverse("budget-detail", kwargs={"pk": budget.pk})
        response = authenticated_client_member.get(url, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            "id": budget.pk,
            "name": budget.name,
            "owner": user_owner.pk,
            "users": [user_member.pk],
        }

    def test_retrieve_budget_anonymous(
        self, anonymous_client: APIClient, budget: Budget
    ):
        """Test retrieve budget anonymous should fail."""
        url = reverse("budget-detail", kwargs={"pk": budget.pk})
        response = anonymous_client.get(url, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_retrieve_budget_not_member_user(
        self, authenticated_client_not_member: APIClient, budget: Budget
    ):
        """Test retrieve budget by user is not member and not owner should fail."""
        url = reverse("budget-detail", kwargs={"pk": budget.pk})
        response = authenticated_client_not_member.get(url, format="json")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_list_budgets_user_owner(
        self,
        authenticated_client_owner: APIClient,
        budget: Budget,
        user_owner: User,
        user_member: User,
    ):
        """Test list budgets by owner."""
        url = reverse("budget-list")
        response = authenticated_client_owner.get(url, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data == [
            {
                "id": budget.pk,
                "name": budget.name,
                "owner": user_owner.pk,
                "users": [user_member.pk],
            }
        ]

    def test_list_budgets_user_member(
        self,
        authenticated_client_member: APIClient,
        budget: Budget,
        user_owner: User,
        user_member: User,
    ):
        """Test list budgets by member."""
        url = reverse("budget-list")
        response = authenticated_client_member.get(url, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data == [
            {
                "id": budget.pk,
                "name": budget.name,
                "owner": user_owner.pk,
                "users": [user_member.pk],
            }
        ]

    def test_list_budgets_anonymous(
        self, anonymous_client: APIClient, budget: Budget
    ):
        """Test list budgets by anonymous should fail."""
        url = reverse("budget-list")
        response = anonymous_client.get(url, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_budgets_not_member_user(
        self, authenticated_client_not_member: APIClient, budget: Budget
    ):
        """Test list budgets by user is not member and not owner should fail."""
        url = reverse("budget-list")
        response = authenticated_client_not_member.get(url, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data == []

    def test_destroy_budget_user_owner(
        self,
        authenticated_client_owner: APIClient,
        user_owner: User,
        budget: Budget,
    ):
        """Test destroy budget by owner."""
        url = reverse("budget-detail", kwargs={"pk": budget.pk})
        response = authenticated_client_owner.delete(url, format="json")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Budget.objects.filter(pk=budget.pk).exists()

    def test_destroy_budget_anonymous(
        self, anonymous_client: APIClient, budget: Budget
    ):
        """Test destroy budget by anonymous should fail."""
        url = reverse("budget-detail", kwargs={"pk": budget.pk})
        response = anonymous_client.delete(url, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert Budget.objects.filter(pk=budget.pk).exists()

    def test_destroy_budget_user_is_not_owner(
        self, authenticated_client_member: APIClient, budget: Budget
    ):
        """Test destroy budget by user is not owner should fail."""
        url = reverse("budget-detail", kwargs={"pk": budget.pk})
        response = authenticated_client_member.delete(url, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Budget.objects.filter(pk=budget.pk).exists()
