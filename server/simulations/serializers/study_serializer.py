from rest_framework import serializers

from simulations.models import Study, StudyViews


class _StudyViewSubSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyViews
        fields = ["id", "asset", "x_axis", "y_axis"]
        read_only_fields = fields


class StudySerializer(serializers.ModelSerializer):
    holdings_count = serializers.SerializerMethodField()
    views = _StudyViewSubSerializer(many=True, read_only=True)

    class Meta:
        model = Study
        fields = [
            "id",
            "title",
            "start_date",
            "end_date",
            "created_by",
            "created_at",
            "holdings_count",
            "views",
        ]
        read_only_fields = ["id", "created_by", "created_at"]

    def get_holdings_count(self, study):
        if not hasattr(study, "portfolio"):
            return 0
        return study.portfolio.holdings.count()
