from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.tokens import RefreshToken

from django.db.models import Q

from family_budget.serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
)
from family_budget.models import Budget
from family_budget.serializers import BudgetSerializer


class UserViewSet(viewsets.ViewSet):
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
                    "refresh_token": str(refresh),
                    "access_token": str(refresh.access_token),
                }
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False, methods=["post"], permission_classes=[IsAuthenticated]
    )
    def logout(self, request):
        """Logout a user."""
        refresh_token = request.data["refresh_token"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response(
            {"message": "User logged out successfully"},
            status=status.HTTP_200_OK,
        )


class BudgetViewSet(viewsets.ModelViewSet):
    """Budget viewset."""

    serializer_class = BudgetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return budgets if current user is owner or member.'"""
        user = self.request.user
        return Budget.objects.filter(Q(owner=user) | Q(users=user))

    def perform_create(self, serializer):
        """Set current user as owner of created budget."""
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        """Check if current user is owner of updated budget."""
        budget = self.get_object()
        if budget.owner != self.request.user:
            raise PermissionDenied(
                "You do not have permission to edit this budget."
            )
        serializer.save()

    def perform_destroy(self, instance):
        """Check if current user is owner of deleted budget."""
        if instance.owner != self.request.user:
            raise PermissionDenied(
                "You do not have permission to delete this budget."
            )
        instance.delete()
