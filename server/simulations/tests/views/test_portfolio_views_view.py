from datetime import date
from decimal import Decimal
from unittest import mock

from rest_framework import status
from rest_framework.test import APITestCase

from core.factories import UserFactory
from simulations.factories import PortfolioFactory, PortfolioHoldingsFactory
from simulations.models import PortfolioViews


class PortfolioViewsViewSetCreateDestroyTests(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.other_user = UserFactory()
        self.client.force_authenticate(user=self.user)
        self.portfolio = PortfolioFactory(created_by=self.user)

    def test_create_creates_view_for_owned_portfolio(self):
        response = self.client.post(
            "/simulations/portfolio_views/", {"portfolio": self.portfolio.id, "y_axis": "value"}
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.portfolio.views.count(), 1)

    def test_create_on_other_users_portfolio_is_forbidden(self):
        other_portfolio = PortfolioFactory(created_by=self.other_user)

        response = self.client.post(
            "/simulations/portfolio_views/", {"portfolio": other_portfolio.id, "y_axis": "value"}
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(other_portfolio.views.count(), 0)

    def test_destroy_own_view_returns_204(self):
        view = PortfolioViews.objects.create(portfolio=self.portfolio)

        response = self.client.delete(f"/simulations/portfolio_views/{view.id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(PortfolioViews.objects.filter(id=view.id).exists())

    def test_destroy_other_users_view_returns_404(self):
        other_portfolio = PortfolioFactory(created_by=self.other_user)
        other_view = PortfolioViews.objects.create(portfolio=other_portfolio)

        response = self.client.delete(f"/simulations/portfolio_views/{other_view.id}/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(PortfolioViews.objects.filter(id=other_view.id).exists())


class PortfolioViewsViewSetPerformanceTests(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.other_user = UserFactory()
        self.client.force_authenticate(user=self.user)
        self.portfolio = PortfolioFactory(
            created_by=self.user, start_date=date(2024, 1, 1), end_date=date(2024, 1, 2)
        )
        self.holding = PortfolioHoldingsFactory(
            portfolio=self.portfolio,
            ticker="AAPL",
            quantity=Decimal("10"),
            cost_per_share=Decimal("10.00"),
            date_purchased=date(2024, 1, 1),
        )

    @mock.patch("simulations.services.performance_service.AssetPriceService.get_price_history")
    def test_performance_returns_computed_series(self, mock_get_price_history):
        mock_get_price_history.return_value = {
            date(2024, 1, 1): Decimal("10.00"),
            date(2024, 1, 2): Decimal("12.00"),
        }
        view = PortfolioViews.objects.create(portfolio=self.portfolio)

        response = self.client.get(f"/simulations/portfolio_views/{view.id}/performance/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["date"], "2024-01-01")
        self.assertEqual(Decimal(response.data[0]["value"]), Decimal("100.00"))
        self.assertEqual(response.data[1]["date"], "2024-01-02")
        self.assertEqual(Decimal(response.data[1]["value"]), Decimal("120.00"))

    @mock.patch("simulations.services.performance_service.AssetPriceService.get_price_history")
    def test_performance_filters_by_view_asset(self, mock_get_price_history):
        mock_get_price_history.return_value = {
            date(2024, 1, 1): Decimal("10.00"),
            date(2024, 1, 2): Decimal("10.00"),
        }
        view = PortfolioViews.objects.create(portfolio=self.portfolio, asset="MSFT")

        response = self.client.get(f"/simulations/portfolio_views/{view.id}/performance/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_performance_for_other_users_view_returns_404(self):
        other_portfolio = PortfolioFactory(created_by=self.other_user)
        other_view = PortfolioViews.objects.create(portfolio=other_portfolio)

        response = self.client.get(f"/simulations/portfolio_views/{other_view.id}/performance/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
