from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from simulations.models import PortfolioHoldings, PortfolioViews
from simulations.serializers import PortfolioPerformanceSerializer, PortfolioViewsSerializer
from simulations.services import PortfolioPerformanceCalculator


class PortfolioViewsViewSet(viewsets.ModelViewSet):
    serializer_class = PortfolioViewsSerializer

    def get_queryset(self):
        return PortfolioViews.objects.filter(portfolio__created_by=self.request.user)

    def perform_create(self, serializer):
        if serializer.validated_data["portfolio"].created_by != self.request.user:
            raise PermissionDenied("You do not have access to this portfolio.")
        serializer.save()

    def performance(self, request, *args, **kwargs):
        view = self.get_object()
        portfolio = view.portfolio

        holdings = PortfolioHoldings.objects.filter(portfolio=portfolio)
        if view.asset:
            holdings = holdings.filter(ticker=view.asset)

        series = PortfolioPerformanceCalculator(
            holdings, portfolio.start_date, portfolio.end_date
        ).compute()
        serializer = PortfolioPerformanceSerializer(series, many=True)
        return Response(serializer.data)
