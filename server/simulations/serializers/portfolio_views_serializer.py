from rest_framework import serializers

from simulations.models import PortfolioViews


class PortfolioViewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioViews
        fields = ["id", "portfolio", "asset", "x_axis", "y_axis"]
        read_only_fields = ["id"]
