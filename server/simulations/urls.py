from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("portfolios", views.PortfolioViewSet, basename="portfolio")
router.register("portfolio_holdings", views.PortfolioHoldingsViewSet, basename="portfolio-holdings")

urlpatterns = router.urls + [
    path(
        "portfolio_views/",
        views.PortfolioViewsViewSet.as_view({"post": "create"}),
        name="portfolio-views-list",
    ),
    path(
        "portfolio_views/<int:pk>/",
        views.PortfolioViewsViewSet.as_view({"delete": "destroy"}),
        name="portfolio-views-detail",
    ),
    path(
        "portfolio_views/<int:pk>/performance/",
        views.PortfolioViewsViewSet.as_view({"get": "performance"}),
        name="portfolio-views-performance",
    ),
]
