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


class ConsolidatedPortfolioHoldingSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    portfolio = serializers.IntegerField()
    ticker = serializers.CharField()
    quantity = serializers.DecimalField(max_digits=16, decimal_places=6)
    cost_per_share = serializers.DecimalField(max_digits=10, decimal_places=2)
    date_purchased = serializers.CharField()
    date_sold = serializers.DateField(allow_null=True)
    current_share_price = serializers.DecimalField(max_digits=10, decimal_places=2, allow_null=True)
    total_cost = serializers.DecimalField(max_digits=18, decimal_places=2)
    total_value = serializers.DecimalField(max_digits=18, decimal_places=2, allow_null=True)
    profit_loss = serializers.DecimalField(max_digits=18, decimal_places=2, allow_null=True)
