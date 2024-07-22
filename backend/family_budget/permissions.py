from rest_framework import permissions

from family_budget.models import Budget


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Custom permission to only allow owners to edit or delete their budgets."""

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        if request.method in permissions.SAFE_METHODS:
            return request.user in obj.users.all()
        return False


class IsOwnerOrUserInBudget(permissions.BasePermission):
    """Custom permission to only allow owners and related users to add/edit incomes/expense of their budgets."""

    def has_permission(self, request, view):
        budget_id = request.data.get("budget")
        if not budget_id:
            return False

        try:
            budget = Budget.objects.get(pk=budget_id)
        except Budget.DoesNotExist:
            return False

        if budget.owner == request.user or request.user in budget.users.all():
            return True
        return False
