from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from simulations.models import Portfolio, PortfolioHoldings
from simulations.serializers import (
    ConsolidatedPortfolioHoldingSerializer,
    PortfolioHoldingsSerializer,
)
from simulations.services import CsvImportService


class PortfolioHoldingsViewSet(viewsets.ModelViewSet):
    serializer_class = PortfolioHoldingsSerializer

    def _get_portfolio(self, portfolio_id):
        return get_object_or_404(Portfolio, pk=portfolio_id, created_by=self.request.user)

    def get_queryset(self):
        portfolio_id = self.request.query_params.get("portfolio")
        if not portfolio_id:
            raise ValidationError({"portfolio": "This query parameter is required."})

        queryset = PortfolioHoldings.objects.filter(portfolio=self._get_portfolio(portfolio_id))

        ticker = self.request.query_params.get("ticker")
        if ticker:
            queryset = queryset.filter(ticker=ticker)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if request.query_params.get("consolidate") in ("1", "true", "True"):
            consolidated = PortfolioHoldings.consolidate_by_ticker(queryset)
            serializer = ConsolidatedPortfolioHoldingSerializer(consolidated, many=True)
            return Response(serializer.data)

        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        portfolio_id = self.request.data.get("portfolio")
        if not portfolio_id:
            raise ValidationError({"portfolio": "This field is required."})
        serializer.save(portfolio=self._get_portfolio(portfolio_id))

    @action(detail=False, methods=["post"])
    def upload(self, request, *args, **kwargs):
        source = request.data.get("source")
        file = request.FILES.get("file")
        portfolio_id = request.data.get("portfolio")

        if not portfolio_id:
            return Response(
                {"detail": "portfolio is required."}, status=status.HTTP_400_BAD_REQUEST
            )

        import_service = CsvImportService(source, file)
        if not import_service.is_supported():
            return Response({"detail": "Unsupported source."}, status=status.HTTP_400_BAD_REQUEST)
        if not file:
            return Response({"detail": "No file provided."}, status=status.HTTP_400_BAD_REQUEST)

        portfolio = self._get_portfolio(portfolio_id)
        rows = import_service.parse()

        created = []
        for row in rows:
            serializer = PortfolioHoldingsSerializer(data=row)
            serializer.is_valid(raise_exception=True)
            created.append(serializer.save(portfolio=portfolio))

        return Response(
            PortfolioHoldingsSerializer(created, many=True).data, status=status.HTTP_201_CREATED
        )
