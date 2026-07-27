from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from simulations.models import Portfolio, PortfolioHoldings, Study
from simulations.serializers import PortfolioHoldingsSerializer


class PortfolioHoldingsViewSet(viewsets.ModelViewSet):
    serializer_class = PortfolioHoldingsSerializer

    def _get_study(self):
        return get_object_or_404(Study, pk=self.kwargs["study_pk"], created_by=self.request.user)

    def get_queryset(self):
        return PortfolioHoldings.objects.filter(portfolio__study=self._get_study())

    def perform_create(self, serializer):
        portfolio, _ = Portfolio.objects.get_or_create(study=self._get_study())
        serializer.save(portfolio=portfolio)
