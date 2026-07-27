from rest_framework import permissions, viewsets

from simulations.models import Study
from simulations.serializers import StudySerializer


class _CanViewStudy(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.created_by == request.user

class StudyViewSet(
    viewsets.ModelViewSet
):
    serializer_class = StudySerializer
    permission_classes = [_CanViewStudy]

    def get_queryset(self):
        return Study.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
