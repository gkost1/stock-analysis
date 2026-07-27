from django.db import models

from .base_model import BaseModel


class Portfolio(BaseModel):
    initial_investment = models.DecimalField(decimal_places=2, max_digits=10)
