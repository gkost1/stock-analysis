from rest_framework import permissions, viewsets

from simulations.models import Portfolio
from simulations.serializers import PortfolioSerializer


class _CanViewPortfolio(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.created_by == request.user


class PortfolioViewSet(viewsets.ModelViewSet):
    serializer_class = PortfolioSerializer
    permission_classes = [_CanViewPortfolio]

    def get_queryset(self):
        return Portfolio.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
