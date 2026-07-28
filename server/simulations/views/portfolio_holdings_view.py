from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.response import Response

from simulations.models import Portfolio, PortfolioHoldings, Study
from simulations.serializers import PortfolioHoldingsSerializer
from simulations.services import CsvImportService


class PortfolioHoldingsViewSet(viewsets.ModelViewSet):
    serializer_class = PortfolioHoldingsSerializer

    def _get_study(self):
        return get_object_or_404(Study, pk=self.kwargs["study_pk"], created_by=self.request.user)

    def get_queryset(self):
        return PortfolioHoldings.objects.filter(portfolio__study=self._get_study())

    def perform_create(self, serializer):
        portfolio, _ = Portfolio.objects.get_or_create(study=self._get_study())
        serializer.save(portfolio=portfolio)

    def upload(self, request, *args, **kwargs):
        source = request.data.get("source")
        file = request.FILES.get("file")

        import_service = CsvImportService(source, file)
        if not import_service.is_supported():
            return Response({"detail": "Unsupported source."}, status=status.HTTP_400_BAD_REQUEST)
        if not file:
            return Response({"detail": "No file provided."}, status=status.HTTP_400_BAD_REQUEST)

        portfolio, _ = Portfolio.objects.get_or_create(study=self._get_study())
        rows = import_service.parse()

        created = []
        for row in rows:
            serializer = PortfolioHoldingsSerializer(data=row)
            serializer.is_valid(raise_exception=True)
            created.append(serializer.save(portfolio=portfolio))

        return Response(PortfolioHoldingsSerializer(created, many=True).data, status=status.HTTP_201_CREATED)
