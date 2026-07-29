from decimal import Decimal

from django.db import models

from simulations.services import AssetPriceService

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
        return AssetPriceService.get_current_price(self.ticker)

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

    @classmethod
    def consolidate_by_ticker(cls, holdings):
        lots_by_ticker = {}
        for holding in holdings:
            lots_by_ticker.setdefault(holding.ticker, []).append(holding)

        return [
            ConsolidatedPortfolioHolding(ticker, lots) for ticker, lots in lots_by_ticker.items()
        ]


class ConsolidatedPortfolioHolding:
    def __init__(self, ticker, lots):
        self.id = lots[0].id
        self.portfolio = lots[0].portfolio_id
        self.ticker = ticker
        self.lots = lots

    @property
    def quantity(self):
        return sum(lot.quantity for lot in self.lots)

    @property
    def cost_per_share(self):
        quantity = self.quantity
        return self.total_cost / quantity if quantity else Decimal("0")

    @property
    def date_purchased(self):
        return "varies" if len(self.lots) > 1 else self.lots[0].date_purchased.isoformat()

    @property
    def date_sold(self):
        return None

    @property
    def current_share_price(self):
        for lot in self.lots:
            if lot.current_share_price is not None:
                return lot.current_share_price
        return None

    @property
    def total_cost(self):
        return sum(lot.total_cost for lot in self.lots)

    @property
    def total_value(self):
        values = [lot.total_value for lot in self.lots]
        return None if any(value is None for value in values) else sum(values)

    @property
    def profit_loss(self):
        value = self.total_value
        return value - self.total_cost if value is not None else None
