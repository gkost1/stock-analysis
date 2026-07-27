from django.db import models

from simulations.services import get_current_price

from .base_model import BaseModel


class PortfolioHoldings(BaseModel):
    portfolio = models.ForeignKey(
        "simulations.Portfolio", on_delete=models.CASCADE, related_name="holdings"
    )
    ticker = models.CharField(max_length=8)
    quantity = models.DecimalField(max_digits=16, decimal_places=6)
    cost_per_share = models.DecimalField(max_digits=10, decimal_places=2)
    date_purchased = models.DateField()
    date_sold = models.DateField(null=True, blank=True)

    @property
    def current_share_price(self):
        return get_current_price(self.ticker)

    @property
    def total_cost(self):
        return self.cost_per_share * self.quantity

    @property
    def total_value(self):
        price = self.current_share_price
        return price * self.quantity if price is not None else None

    @property
    def profit_loss(self):
        value = self.total_value
        return value - self.total_cost if value is not None else None
