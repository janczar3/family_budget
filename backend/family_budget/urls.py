from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from family_budget.views import (
    UserAuthViewSet,
    UserDetailView,
    BudgetViewSet,
    IncomeViewSet,
    ExpenseViewSet,
)

router = DefaultRouter()
router.register(r"users", UserAuthViewSet, basename="user")
router.register(r"budgets", BudgetViewSet, basename="budget")
router.register(r"incomes", IncomeViewSet, basename="income")
router.register(r"expenses", ExpenseViewSet, basename="expense")

urlpatterns = [
    path("", include(router.urls)),
    path("user/", UserDetailView.as_view(), name="user-detail"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
