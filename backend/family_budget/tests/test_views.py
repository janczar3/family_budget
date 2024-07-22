import pytest
from rest_framework import status
from rest_framework.test import APIClient

from django.urls import reverse
from django.contrib.auth.models import User

from family_budget.models import Budget, Income, Expense
from family_budget.taxonomies import ExpenseCategory, IncomeCategory
from family_budget.tests.base import TestBudgetBase


@pytest.mark.django_db
class TestUserAuthViewSet:
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
        assert "access" in response.data
        assert "refresh" in response.data

    def test_login_user_not_exists(self, client: APIClient, login_url: str):
        """Test login user not exists."""
        data = {
            "username": "wronguser",
            "password": "wrongpassword",
        }
        response = client.post(login_url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestBudgetViewSet(TestBudgetBase):
    """Test BudgetViewSet and depended serializer."""

    @pytest.fixture
    def url_detail(self, budget) -> callable:
        return reverse("budget-detail", kwargs={"pk": budget.pk})

    @pytest.fixture
    def url_list(self) -> str:
        return reverse("budget-list")

    def test_create_budget(
        self,
        authenticated_client_owner: APIClient,
        user_owner: User,
        url_list: str,
    ):
        """Test create budget."""
        data = {
            "name": "budget_1",
        }
        response = authenticated_client_owner.post(
            url_list, data, format="json"
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["name"] == data["name"]
        assert response.data["owner"] == user_owner.pk
        assert Budget.objects.filter(name=data["name"]).exists()

    def test_create_budget_anonymous(
        self, anonymous_client: APIClient, url_list: str
    ):
        """Test create budget anonymous should fail."""
        data = {
            "name": "budget_1",
        }
        response = anonymous_client.post(url_list, data, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert not Budget.objects.filter(name=data["name"]).exists()

    def test_update_budget(
        self,
        authenticated_client_owner: APIClient,
        user_owner: User,
        budget: Budget,
        url_detail: str,
    ):
        """Test update budget."""
        data = {"name": "new_budget_name"}
        response = authenticated_client_owner.patch(
            url_detail, data, format="json"
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == data["name"]
        assert response.data["owner"] == user_owner.pk
        assert Budget.objects.filter(name=data["name"]).exists()

    def test_update_budget_anonymous(
        self, anonymous_client: APIClient, budget: Budget, url_detail: str
    ):
        """Test update budget anonymous should fail."""
        data = {"name": "new_budget_name"}
        response = anonymous_client.patch(url_detail, data, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert not Budget.objects.filter(name=data["name"]).exists()

    def test_update_budget_user_is_not_owner(
        self,
        authenticated_client_member: APIClient,
        budget: Budget,
        url_detail: str,
    ):
        """Test update budget by member only should fail."""
        data = {"name": "new_budget_name"}
        response = authenticated_client_member.patch(
            url_detail, data, format="json"
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert not Budget.objects.filter(name=data["name"]).exists()

    def test_retrieve_budget_user_is_owner(
        self,
        authenticated_client_owner: APIClient,
        budget: Budget,
        user_owner: User,
        user_member: User,
        url_detail: str,
    ):
        """Test retrieve budget by owner."""
        response = authenticated_client_owner.get(url_detail, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            "id": budget.pk,
            "name": budget.name,
            "owner": user_owner.pk,
            "users": [user_member.pk],
            "expenses": [],
            "incomes": [],
            "total": 0,
        }

    def test_retrieve_budget_user_is_member(
        self,
        authenticated_client_member: APIClient,
        budget: Budget,
        user_owner: User,
        user_member: User,
        url_detail: str,
    ):
        """Test retrieve budget by member."""
        response = authenticated_client_member.get(url_detail, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            "id": budget.pk,
            "name": budget.name,
            "owner": user_owner.pk,
            "users": [user_member.pk],
            "expenses": [],
            "incomes": [],
            "total": 0,
        }

    def test_retrieve_budget_anonymous(
        self, anonymous_client: APIClient, budget: Budget, url_detail: str
    ):
        """Test retrieve budget anonymous should fail."""
        response = anonymous_client.get(url_detail, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_retrieve_budget_not_member_user(
        self,
        authenticated_client_not_member: APIClient,
        budget: Budget,
        url_detail,
    ):
        """Test retrieve budget by user is not member and not owner should fail."""
        response = authenticated_client_not_member.get(
            url_detail, format="json"
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_list_budgets_user_owner(
        self,
        authenticated_client_owner: APIClient,
        budget: Budget,
        user_owner: User,
        user_member: User,
        url_list: str,
    ):
        """Test list budgets by owner."""
        response = authenticated_client_owner.get(url_list, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [
                {
                    "id": budget.pk,
                    "name": budget.name,
                    "owner": user_owner.pk,
                    "users": [user_member.pk],
                    "expenses": [],
                    "incomes": [],
                    "total": 0,
                }
            ]
        }

    def test_list_budgets_user_member(
        self,
        authenticated_client_member: APIClient,
        budget: Budget,
        user_owner: User,
        user_member: User,
        url_list: str,
    ):
        """Test list budgets by member."""
        response = authenticated_client_member.get(url_list, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            'count': 1,
            'next': None,
            'previous': None,
            'results':  [
                {
                    "id": budget.pk,
                    "name": budget.name,
                    "owner": user_owner.pk,
                    "users": [user_member.pk],
                    "expenses": [],
                    "incomes": [],
                    "total": 0,
                }
            ]
        }

    def test_list_budgets_anonymous(
        self,
        anonymous_client: APIClient,
        budget: Budget,
        url_list: str,
    ):
        """Test list budgets by anonymous should fail."""
        response = anonymous_client.get(url_list, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_budgets_not_member_user(
        self,
        authenticated_client_not_member: APIClient,
        budget: Budget,
        url_list: str,
    ):
        """Test list budgets by user is not member and not owner should fail."""
        response = authenticated_client_not_member.get(url_list, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            'count': 0,
            'next': None,
            'previous': None,
            'results': [],
        }

    def test_destroy_budget_user_owner(
        self,
        authenticated_client_owner: APIClient,
        user_owner: User,
        budget: Budget,
        url_detail: str,
    ):
        """Test destroy budget by owner."""
        response = authenticated_client_owner.delete(url_detail, format="json")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Budget.objects.filter(pk=budget.pk).exists()

    def test_destroy_budget_anonymous(
        self, anonymous_client: APIClient, budget: Budget, url_detail: str
    ):
        """Test destroy budget by anonymous should fail."""
        response = anonymous_client.delete(url_detail, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert Budget.objects.filter(pk=budget.pk).exists()

    def test_destroy_budget_user_is_not_owner(
        self,
        authenticated_client_member: APIClient,
        budget: Budget,
        url_detail: str,
    ):
        """Test destroy budget by user is not owner should fail."""
        response = authenticated_client_member.delete(url_detail, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Budget.objects.filter(pk=budget.pk).exists()


@pytest.mark.django_db
class TestIncomeViewSet(TestBudgetBase):
    """Test IncomeViewSet and depended serializer."""

    @pytest.fixture
    def url_list(self) -> str:
        return reverse("income-list")

    @pytest.mark.parametrize(
        "user_type,status_code",
        [
            ("owner", status.HTTP_201_CREATED),
            ("member", status.HTTP_201_CREATED),
            ("not_member", status.HTTP_403_FORBIDDEN),
            ("anonymous", status.HTTP_401_UNAUTHORIZED),
        ],
    )
    def test_add_income(
        self,
        authenticated_client_owner: APIClient,
        authenticated_client_member: APIClient,
        authenticated_client_not_member: APIClient,
        anonymous_client: APIClient,
        budget: Budget,
        url_list: str,
        user_type: str,
        status_code: status,
    ):
        user_type_client_map = {
            "owner": authenticated_client_owner,
            "member": authenticated_client_member,
            "not_member": authenticated_client_not_member,
            "anonymous": anonymous_client,
        }
        client = user_type_client_map.get(user_type)
        data = {
            "name": "income_1",
            "budget": budget.pk,
            "value": 100.23,
            "category": IncomeCategory.SALARY.value,
        }
        response = client.post(url_list, data=data, format="json")

        assert response.status_code == status_code
        if status_code == status.HTTP_201_CREATED:
            income = Income.objects.get(pk=response.data["id"])
            assert income
            assert response.data == {
                "budget": budget.pk,
                "id": income.pk,
                "name": data["name"],
                "value": str(data["value"]),
                "category": IncomeCategory.SALARY.value,
            }

    # todo tests


@pytest.mark.django_db
class TestExpenseViewSet(TestBudgetBase):
    """Test ExpenseViewSet and depended serializer."""

    @pytest.fixture
    def url_list(self) -> str:
        return reverse("expense-list")

    @pytest.mark.parametrize(
        "user_type,status_code",
        [
            ("owner", status.HTTP_201_CREATED),
            ("member", status.HTTP_201_CREATED),
            ("not_member", status.HTTP_403_FORBIDDEN),
            ("anonymous", status.HTTP_401_UNAUTHORIZED),
        ],
    )
    def test_add_expense(
        self,
        authenticated_client_owner: APIClient,
        authenticated_client_member: APIClient,
        authenticated_client_not_member: APIClient,
        anonymous_client: APIClient,
        budget: Budget,
        url_list: str,
        user_type: str,
        status_code: status,
    ):
        user_type_client_map = {
            "owner": authenticated_client_owner,
            "member": authenticated_client_member,
            "not_member": authenticated_client_not_member,
            "anonymous": anonymous_client,
        }
        client = user_type_client_map.get(user_type)
        data = {
            "name": "expense_1",
            "budget": budget.pk,
            "value": 100.23,
            "category": ExpenseCategory.GROCERIES.value,
        }
        response = client.post(url_list, data=data, format="json")

        assert response.status_code == status_code
        if status_code == status.HTTP_201_CREATED:
            expense = Expense.objects.get(pk=response.data["id"])
            assert expense
            assert response.data == {
                "budget": budget.pk,
                "id": expense.pk,
                "name": data["name"],
                "value": str(data["value"]),
                "category": ExpenseCategory.GROCERIES.value,
            }

    # todo tests
