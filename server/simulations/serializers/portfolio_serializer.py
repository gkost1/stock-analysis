from rest_framework import serializers

from simulations.models import Portfolio, PortfolioViews


class _PortfolioViewSubSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioViews
        fields = ["id", "asset", "x_axis", "y_axis"]
        read_only_fields = fields


class PortfolioSerializer(serializers.ModelSerializer):
    holdings_count = serializers.SerializerMethodField()
    views = _PortfolioViewSubSerializer(many=True, read_only=True)

    class Meta:
        model = Portfolio
        fields = [
            "id",
            "title",
            "start_date",
            "end_date",
            "created_by",
            "created_at",
            "initial_investment",
            "holdings_count",
            "views",
        ]
        read_only_fields = ["id", "created_by", "created_at"]

    def get_holdings_count(self, portfolio):
        return portfolio.holdings.count()
