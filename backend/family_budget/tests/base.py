import pytest
from rest_framework.test import APIClient
from django_dynamic_fixture import G

from django.contrib.auth.models import User

from family_budget.models import Budget


class TestBudgetBase:
    """Base class for test budget, incomes, expenses."""

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
