from django.db import models

from .base_model import BaseModel


class CachedTickerPrice(BaseModel):
    ticker = models.CharField(max_length=8, unique=True)
    price = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
