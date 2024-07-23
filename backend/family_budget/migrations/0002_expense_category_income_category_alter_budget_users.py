# Generated by Django 5.0.7 on 2024-07-23 19:21

import family_budget.taxonomies
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("family_budget", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="expense",
            name="category",
            field=models.CharField(
                choices=[
                    ("groceries", "GROCERIES"),
                    ("restaurant", "RESTAURANT"),
                    ("entertainment", "ENTERTAINMENT"),
                    ("home", "HOME"),
                    ("medicines", "MEDICINES"),
                    ("children", "CHILDREN"),
                    ("investments", "INVESTMENTS"),
                    ("pets", "PETS"),
                    ("car", "CAR"),
                    ("bill", "BILL"),
                    ("other", "OTHER"),
                ],
                default=family_budget.taxonomies.ExpenseCategory["OTHER"],
                max_length=32,
            ),
        ),
        migrations.AddField(
            model_name="income",
            name="category",
            field=models.CharField(
                choices=[
                    ("salary", "SALARY"),
                    ("savings", "SAVINGS"),
                    ("other", "OTHER"),
                ],
                default=family_budget.taxonomies.IncomeCategory["OTHER"],
                max_length=32,
            ),
        ),
        migrations.AlterField(
            model_name="budget",
            name="users",
            field=models.ManyToManyField(
                blank=True,
                null=True,
                related_name="shared_budgets",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
