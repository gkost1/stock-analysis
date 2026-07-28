from django.conf import settings
from django.db import models

from .base_model import BaseModel


class Portfolio(BaseModel):
    title = models.CharField(max_length=128, default="")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    initial_investment = models.DecimalField(decimal_places=2, max_digits=10, default=0)
