from django.contrib.auth.models import User
from django.db import models


class Budget(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="budgets"
    )
    users = models.ManyToManyField(
        User, related_name="shared_budgets", blank=True, null=True
    )


class Income(models.Model):
    name = models.CharField(max_length=100)
    budget = models.ForeignKey(
        "Budget", on_delete=models.CASCADE, related_name="incomes"
    )
    value = models.DecimalField(max_digits=10, decimal_places=2)


class Expense(models.Model):
    name = models.CharField(max_length=100)
    budget = models.ForeignKey(
        "Budget", on_delete=models.CASCADE, related_name="expenses"
    )
    value = models.DecimalField(max_digits=10, decimal_places=2)
