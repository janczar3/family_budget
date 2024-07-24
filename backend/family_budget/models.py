from django.contrib.auth.models import User
from django.db import models

from family_budget.taxonomies import ExpenseCategory, IncomeCategory


class Budget(models.Model):
    """Represents a budget which can be managed by an owner and shared with other users.

    Attributes:
        name (str): The name of the budget.
        owner (User): The owner of the budget.
        users (ManyToManyField): Users who have access to the budget.
    """

    name = models.CharField(max_length=100)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="budgets"
    )
    users = models.ManyToManyField(
        User, related_name="shared_budgets", blank=True, null=True
    )


class Income(models.Model):
    """Represents an income entry in a budget.

    Attributes:
        name (str): The name of the income.
        budget (Budget): The budget to which this income belongs.
        value (Decimal): The value of the income.
        category (str): The category of the income, chosen from IncomeCategory.
    """

    name = models.CharField(max_length=100)
    budget = models.ForeignKey(
        "Budget", on_delete=models.CASCADE, related_name="incomes"
    )
    value = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(
        choices=IncomeCategory.choices(),
        default=IncomeCategory.OTHER,
        max_length=32,
    )


class Expense(models.Model):
    """Represents an expense entry in a budget.

    Attributes:
        name (str): The name of the expense.
        budget (Budget): The budget to which this expense belongs.
        value (Decimal): The value of the expense.
        category (str): The category of the expense, chosen from ExpenseCategory.
    """

    name = models.CharField(max_length=100)
    budget = models.ForeignKey(
        "Budget", on_delete=models.CASCADE, related_name="expenses"
    )
    value = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(
        choices=ExpenseCategory.choices(),
        default=ExpenseCategory.OTHER,
        max_length=32,
    )
