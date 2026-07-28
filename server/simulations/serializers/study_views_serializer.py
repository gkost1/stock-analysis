from rest_framework import serializers

from simulations.models import StudyViews


class StudyViewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyViews
        fields = ["id", "study", "asset", "x_axis", "y_axis"]
        read_only_fields = ["id"]
