from django.urls import path, include
from rest_framework.routers import DefaultRouter
from family_budget.views import (
    UserViewSet,
    BudgetViewSet,
    IncomeViewSet,
    ExpenseViewSet,
)

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"budgets", BudgetViewSet, basename="budget")
router.register(r"incomes", IncomeViewSet, basename="income")
router.register(r"expenses", ExpenseViewSet, basename="expense")

urlpatterns = [
    path("", include(router.urls)),
]
