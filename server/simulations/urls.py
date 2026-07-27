from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("studies", views.StudyViewSet, basename="study")

urlpatterns = router.urls + [
    path(
        "studies/<int:study_pk>/holdings/",
        views.PortfolioHoldingsViewSet.as_view({"get": "list", "post": "create"}),
        name="study-holdings-list",
    ),
    path(
        "studies/<int:study_pk>/holdings/<int:pk>/",
        views.PortfolioHoldingsViewSet.as_view(
            {"get": "retrieve", "patch": "partial_update", "put": "update", "delete": "destroy"}
        ),
        name="study-holdings-detail",
    ),
]
