from rest_framework import mixins, viewsets

from simulations.models import Study
from simulations.serializers import StudySerializer


class StudyViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = StudySerializer

    def get_queryset(self):
        return Study.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
