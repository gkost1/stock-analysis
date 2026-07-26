from django.db import models

from .base_model import BaseModel


class Study(BaseModel):
    start_date = models.DateField()
    end_date = models.DateField()
