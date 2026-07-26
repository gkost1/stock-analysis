from django.db import models
from .base_model import BaseModel

TRANSACTION_TYPE_CHOICES = [
    ("B", "Buy"),
    ("S", "Sell")
]

class PortfolioTransactions(BaseModel):
    portfolio = models.ForeignKey("simulations.Portfolio", on_delete=models.CASCADE, related_name="transactions")
    type = models.CharField(max_length=1, choices=TRANSACTION_TYPE_CHOICES)
    ticker = models.CharField(max_length=8)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.DecimalField(max_digits=16, decimal_places=6)
    date = models.DateField()