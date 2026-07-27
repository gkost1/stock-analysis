from django.db import models

from .base_model import BaseModel

INVESTMENT_FREQUENCY_CHOICES = [
    ("D", "Daily"),
    ("W", "Weekly"),
    ("2W", "Biweekly"),
    ("SM", "Semi-monthly"),
    ("M", "Monthly"),
    ("Q", "Quarterly"),
    ("SA", "Semi-annually"),
    ("Y", "Yearly"),
]


class RecurringInvestments(BaseModel):
    portfolio = models.ForeignKey(
        "simulations.Portfolio", on_delete=models.CASCADE, related_name="recurring_investments"
    )
    frequency = models.CharField(max_length=2, choices=INVESTMENT_FREQUENCY_CHOICES)
    ticker = models.CharField(max_length=8)
    dollar_amount = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)  # no end date means indefinite contribution
