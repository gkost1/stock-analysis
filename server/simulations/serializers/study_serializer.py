from rest_framework import serializers

from simulations.models import Study


class StudySerializer(serializers.ModelSerializer):
    class Meta:
        model = Study
        fields = ["id", "title", "start_date", "end_date", "created_by", "created_at"]
        read_only_fields = ["id", "created_by", "created_at"]
