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


class IsOwnerOrMemberOfBudget(permissions.BasePermission):
    """Custom permission to only allow owners and members to edit or delete their incomes/expenses."""

    def has_object_permission(self, request, view, obj):
        budget_id = request.data.get("budget")
        if budget_id:
            budget = Budget.objects.get(pk=budget_id)
            return (
                budget.owner == request.user
                or request.user in budget.users.all()
            )
        return False
