from decimal import Decimal
from unittest import mock

from rest_framework import status
from rest_framework.test import APITestCase

from core.factories import UserFactory
from simulations.factories import PortfolioFactory, PortfolioHoldingsFactory


class PortfolioHoldingsViewSetTests(APITestCase):
    def setUp(self):
        current_price_patcher = mock.patch(
            "simulations.models.portfolio_holdings.get_current_price",
            return_value=Decimal("100.00"),
        )
        current_price_patcher.start()
        self.addCleanup(current_price_patcher.stop)

        historical_price_patcher = mock.patch(
            "simulations.factories.portfolio_holdings_factory.get_historical_price",
            return_value=Decimal("100.00"),
        )
        historical_price_patcher.start()
        self.addCleanup(historical_price_patcher.stop)

        self.user = UserFactory()
        self.other_user = UserFactory()
        self.client.force_authenticate(user=self.user)
        self.portfolio = PortfolioFactory(created_by=self.user)

    def test_list_only_returns_own_portfolios_holdings(self):
        own_holding = PortfolioHoldingsFactory(portfolio=self.portfolio)

        other_portfolio = PortfolioFactory(created_by=self.other_user)
        PortfolioHoldingsFactory(portfolio=other_portfolio)

        response = self.client.get(
            f"/simulations/portfolio_holdings/?portfolio={self.portfolio.id}"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ids = [holding["id"] for holding in response.data]
        self.assertEqual(ids, [own_holding.id])

    def test_list_without_portfolio_param_returns_400(self):
        response = self.client.get("/simulations/portfolio_holdings/")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_other_users_portfolio_returns_404(self):
        other_portfolio = PortfolioFactory(created_by=self.other_user)

        response = self.client.get(
            f"/simulations/portfolio_holdings/?portfolio={other_portfolio.id}"
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_requires_portfolio_param(self):
        response = self.client.post(
            "/simulations/portfolio_holdings/",
            {
                "ticker": "AAPL",
                "quantity": "10",
                "cost_per_share": "150.00",
                "date_purchased": "2024-01-01",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_creates_holding_for_owned_portfolio(self):
        response = self.client.post(
            "/simulations/portfolio_holdings/",
            {
                "portfolio": self.portfolio.id,
                "ticker": "AAPL",
                "quantity": "10",
                "cost_per_share": "150.00",
                "date_purchased": "2024-01-01",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["portfolio"], self.portfolio.id)
        self.assertEqual(self.portfolio.holdings.count(), 1)

    def test_create_includes_computed_fields(self):
        response = self.client.post(
            "/simulations/portfolio_holdings/",
            {
                "portfolio": self.portfolio.id,
                "ticker": "AAPL",
                "quantity": "10",
                "cost_per_share": "50.00",
                "date_purchased": "2024-01-01",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Decimal(response.data["current_share_price"]), Decimal("100.00"))
        self.assertEqual(Decimal(response.data["total_cost"]), Decimal("500.00"))
        self.assertEqual(Decimal(response.data["total_value"]), Decimal("1000.00"))
        self.assertEqual(Decimal(response.data["profit_loss"]), Decimal("500.00"))

    def test_create_on_other_users_portfolio_returns_404(self):
        other_portfolio = PortfolioFactory(created_by=self.other_user)

        response = self.client.post(
            "/simulations/portfolio_holdings/",
            {
                "portfolio": other_portfolio.id,
                "ticker": "AAPL",
                "quantity": "10",
                "cost_per_share": "150.00",
                "date_purchased": "2024-01-01",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_destroy_other_users_holding_returns_404(self):
        other_portfolio = PortfolioFactory(created_by=self.other_user)
        other_holding = PortfolioHoldingsFactory(portfolio=other_portfolio)

        response = self.client.delete(
            f"/simulations/portfolio_holdings/{other_holding.id}/?portfolio={other_portfolio.id}"
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
