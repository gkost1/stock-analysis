from django.db import models

from .base_model import BaseModel


class Portfolio(BaseModel):
    study = models.OneToOneField(
        "simulations.Study", on_delete=models.CASCADE, related_name="portfolio"
    )
    initial_investment = models.DecimalField(decimal_places=2, max_digits=10, default=0)
