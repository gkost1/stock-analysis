from django.db import models

from .base_model import BaseModel


class PortfolioHoldings(BaseModel):
    portfolio = models.ForeignKey(
        "simulations.Portfolio", on_delete=models.CASCADE, related_name="holdings"
    )
    ticker = models.CharField(max_length=8)
    quantity = models.DecimalField(max_digits=16, decimal_places=6)
