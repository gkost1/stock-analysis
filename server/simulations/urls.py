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
        "studies/<int:study_pk>/holdings/upload/",
        views.PortfolioHoldingsViewSet.as_view({"post": "upload"}),
        name="study-holdings-upload",
    ),
    path(
        "studies/<int:study_pk>/holdings/<int:pk>/",
        views.PortfolioHoldingsViewSet.as_view(
            {"get": "retrieve", "patch": "partial_update", "put": "update", "delete": "destroy"}
        ),
        name="study-holdings-detail",
    ),
    path(
        "study_views/",
        views.StudyViewsViewSet.as_view({"post": "create"}),
        name="study-views-list",
    ),
    path(
        "study_views/<int:pk>/",
        views.StudyViewsViewSet.as_view({"delete": "destroy"}),
        name="study-views-detail",
    ),
    path(
        "study_views/<int:pk>/performance/",
        views.StudyViewsViewSet.as_view({"get": "performance"}),
        name="study-views-performance",
    ),
]
