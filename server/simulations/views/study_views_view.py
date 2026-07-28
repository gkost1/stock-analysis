from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from simulations.models import PortfolioHoldings, StudyViews
from simulations.serializers import PortfolioPerformanceSerializer, StudyViewsSerializer
from simulations.services import PortfolioPerformanceCalculator


class StudyViewsViewSet(viewsets.ModelViewSet):
    serializer_class = StudyViewsSerializer

    def get_queryset(self):
        return StudyViews.objects.filter(study__created_by=self.request.user)

    def perform_create(self, serializer):
        if serializer.validated_data["study"].created_by != self.request.user:
            raise PermissionDenied("You do not have access to this study.")
        serializer.save()

    def performance(self, request, *args, **kwargs):
        view = self.get_object()
        study = view.study

        holdings = PortfolioHoldings.objects.filter(portfolio__study=study)
        if view.asset:
            holdings = holdings.filter(ticker=view.asset)

        series = PortfolioPerformanceCalculator(holdings, study.start_date, study.end_date).compute()
        serializer = PortfolioPerformanceSerializer(series, many=True)
        return Response(serializer.data)
