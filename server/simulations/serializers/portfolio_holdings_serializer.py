from rest_framework import serializers

from simulations.models import PortfolioHoldings


class PortfolioHoldingsSerializer(serializers.ModelSerializer):
    current_share_price = serializers.ReadOnlyField()
    total_cost = serializers.ReadOnlyField()
    total_value = serializers.ReadOnlyField()
    profit_loss = serializers.ReadOnlyField()

    class Meta:
        model = PortfolioHoldings
        fields = [
            "id",
            "portfolio",
            "ticker",
            "quantity",
            "cost_per_share",
            "date_purchased",
            "date_sold",
            "current_share_price",
            "total_cost",
            "total_value",
            "profit_loss",
        ]
        read_only_fields = ["id", "portfolio"]
