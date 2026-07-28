from django.db import models

from .base_model import BaseModel

X_AXIS_CHOICES = [("time", "Time")]
Y_AXIS_CHOICES = [("value", "Value"), ("profit_loss", "Profit/Loss"), ("cagr", "CAGR")]


class StudyViews(BaseModel):
    study = models.ForeignKey("simulations.Study", on_delete=models.CASCADE, related_name="views")
    asset = models.CharField(max_length=8, null=True, blank=True)
    x_axis = models.CharField(max_length=16, choices=X_AXIS_CHOICES, default="time")
    y_axis = models.CharField(max_length=16, choices=Y_AXIS_CHOICES, default="value")
