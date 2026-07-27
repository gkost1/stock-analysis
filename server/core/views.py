from django.conf import settings
from django.contrib.auth import authenticate
from django.http import Http404, HttpResponse
from rest_framework import generics, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from core.factories import UserFactory
from core.serializers import UserSerializer


def index(request):
    return HttpResponse("Hello, world. You're at the core index.")


class RegisterView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {"token": token.key, "user": serializer.data},
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is None:
            return Response(
                {"detail": "Invalid credentials."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user": UserSerializer(user).data})


class LogoutView(APIView):
    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def _seed_factories():
    from simulations.factories import (
        PortfolioFactory,
        PortfolioHoldingsFactory,
        PortfolioTransactionsFactory,
        RecurringInvestmentsFactory,
        StudyFactory,
    )

    return {
        "UserFactory": UserFactory,
        "StudyFactory": StudyFactory,
        "PortfolioFactory": PortfolioFactory,
        "PortfolioHoldingsFactory": PortfolioHoldingsFactory,
        "PortfolioTransactionsFactory": PortfolioTransactionsFactory,
        "RecurringInvestmentsFactory": RecurringInvestmentsFactory,
    }


class SeedView(APIView):
    """Test-only fixture creation endpoint, used by Cypress e2e tests to seed data via factories.

    Disabled unless DEBUG is on, so it can never be reached in a production deployment.
    """

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        if not settings.DEBUG:
            raise Http404

        factory_name = request.data.get("factory")
        factory_class = _seed_factories().get(factory_name)
        if factory_class is None:
            return Response(
                {"detail": f"Unknown factory '{factory_name}'."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        instance = factory_class(**request.data.get("attrs", {}))
        return Response({"id": instance.pk}, status=status.HTTP_201_CREATED)
