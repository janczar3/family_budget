from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView

from django.db.models import Q

from family_budget.models import Budget, Income, Expense
from family_budget.serializers import (
    BudgetSerializer,
    IncomeSerializer,
    ExpenseSerializer,
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserDetailsSerializer,
)
from family_budget.pagination import BudgetPagination
from family_budget.permissions import IsOwnerOrReadOnly, IsOwnerOrUserInBudget


class UserDetailView(APIView):
    """View to get user's details'"""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserDetailsSerializer(request.user)
        return Response(serializer.data)


class UserAuthViewSet(viewsets.ViewSet):
    """ViewSet for register, login and logout users."""

    permission_classes = [AllowAny]

    @action(detail=False, methods=["post"])
    def register(self, request):
        """Register a new user."""
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User registered successfully"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"])
    def login(self, request):
        """Login a user."""
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=["post"],
    )
    def logout(self, request):
        """Logout a user."""
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response(
            {"message": "User logged out successfully"},
            status=status.HTTP_200_OK,
        )


class BudgetViewSet(viewsets.ModelViewSet):
    """Budget viewset to manage budgets."""

    serializer_class = BudgetSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    pagination_class = BudgetPagination

    def get_queryset(self):
        """Return budgets if current user is owner or member.'"""
        user = self.request.user
        return Budget.objects.filter(Q(owner=user) | Q(users=user))

    def perform_create(self, serializer):
        """Set current user as owner of created budget."""
        serializer.save(owner=self.request.user)


class IncomeViewSet(viewsets.ModelViewSet):
    """Income viewset to add, edit and remove incomes."""

    serializer_class = IncomeSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrUserInBudget]


class ExpenseViewSet(viewsets.ModelViewSet):
    """Expense viewset to add, edit and remove expenses."""

    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrUserInBudget]
