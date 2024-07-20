from django.urls import path, include
from rest_framework.routers import DefaultRouter
from family_budget.views import UserViewSet, BudgetViewSet

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"budgets", BudgetViewSet, basename="budget")

urlpatterns = [
    path("", include(router.urls)),
]
