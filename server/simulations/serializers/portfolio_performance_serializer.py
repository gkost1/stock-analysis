from rest_framework import serializers


class PortfolioPerformanceSerializer(serializers.Serializer):
    date = serializers.DateField()
    value = serializers.DecimalField(max_digits=16, decimal_places=2)
    profit_loss = serializers.DecimalField(max_digits=16, decimal_places=2)
    cagr = serializers.DecimalField(max_digits=10, decimal_places=4, allow_null=True)
