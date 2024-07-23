from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password

from family_budget.models import Budget, Income, Expense


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for creating a new user."""

    password = serializers.CharField(
        write_only=True, validators=[validate_password]
    )
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "password", "password_confirm"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        """Validate password and confirm password."""
        if data["password"] != data["password_confirm"]:
            raise serializers.ValidationError(
                {"password_confirm": "Passwords must match"}
            )
        return data

    def create(self, validated_data):
        """Create a new user."""
        user = User(
            username=validated_data["username"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            data["user"] = user
            return data
        raise serializers.ValidationError("Invalid credentials.")


class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ["id", "name", "budget", "value", "category"]


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ["id", "name", "budget", "value", "category"]


class BudgetSerializer(serializers.ModelSerializer):
    incomes = IncomeSerializer(many=True, read_only=True)
    expenses = ExpenseSerializer(many=True, read_only=True)
    users = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        required=False,
        allow_empty=True,
    )
    user_names = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()

    class Meta:
        model = Budget
        fields = [
            "id",
            "name",
            "owner",
            "users",
            "user_names",
            "incomes",
            "expenses",
            "total",
        ]
        read_only_fields = [
            "owner",
            "incomes",
            "expenses",
            "total",
            "user_names",
        ]

    def get_total(self, obj):
        incomes_sum = sum(obj.incomes.values_list("value", flat=True))
        expenses_sum = sum(obj.expenses.values_list("value", flat=True))
        return incomes_sum - expenses_sum

    def get_user_names(self, obj):
        """Represents user names."""
        return [user.username for user in obj.users.all()]

    def create(self, validated_data):
        """Convert user names to their ids."""
        user_ids = None
        if "users" in validated_data:
            user_names = validated_data.pop("users")
            user_ids = User.objects.filter(username__in=user_names).values_list(
                "id", flat=True
            )
        budget = Budget.objects.create(**validated_data)
        if user_ids:
            budget.users.set(user_ids)
        return budget

    def update(self, instance, validated_data):
        """Convert user names to their ids."""
        if "users" in validated_data:
            user_names = validated_data.pop("users")
            user_ids = User.objects.filter(username__in=user_names).values_list(
                "id", flat=True
            )
            instance.users.set(user_ids)
        return super().update(instance, validated_data)


class UserDetailsSerializer(serializers.ModelSerializer):
    own_budgets = serializers.SerializerMethodField()
    shared_budgets = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "email", "own_budgets", "shared_budgets"]

    def get_own_budgets(self, obj):
        own_budgets = Budget.objects.filter(owner=obj)
        return BudgetSerializer(own_budgets, many=True).data

    def get_shared_budgets(self, obj):
        shared_budgets = Budget.objects.filter(users=obj)
        return BudgetSerializer(shared_budgets, many=True).data
