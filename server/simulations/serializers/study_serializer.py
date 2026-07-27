from rest_framework import serializers

from simulations.models import Study


class StudySerializer(serializers.ModelSerializer):
    holdings_count = serializers.SerializerMethodField()

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
        ]
        read_only_fields = ["id", "created_by", "created_at"]

    def get_holdings_count(self, study):
        if not hasattr(study, "portfolio"):
            return 0
        return study.portfolio.holdings.count()
