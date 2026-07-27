from decimal import Decimal
from unittest import mock

from rest_framework import status
from rest_framework.test import APITestCase

from core.factories import UserFactory
from simulations.factories import PortfolioFactory, PortfolioHoldingsFactory, StudyFactory


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
        self.study = StudyFactory(created_by=self.user)

    def test_list_only_returns_own_studys_holdings(self):
        portfolio = PortfolioFactory(study=self.study)
        own_holding = PortfolioHoldingsFactory(portfolio=portfolio)

        other_study = StudyFactory(created_by=self.other_user)
        other_portfolio = PortfolioFactory(study=other_study)
        PortfolioHoldingsFactory(portfolio=other_portfolio)

        response = self.client.get(f"/simulations/studies/{self.study.id}/holdings/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ids = [holding["id"] for holding in response.data]
        self.assertEqual(ids, [own_holding.id])

    def test_list_other_users_study_returns_404(self):
        other_study = StudyFactory(created_by=self.other_user)

        response = self.client.get(f"/simulations/studies/{other_study.id}/holdings/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_creates_portfolio_when_missing(self):
        self.assertFalse(hasattr(self.study, "portfolio"))

        response = self.client.post(
            f"/simulations/studies/{self.study.id}/holdings/",
            {
                "ticker": "AAPL",
                "quantity": "10",
                "cost_per_share": "150.00",
                "date_purchased": "2024-01-01",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.study.refresh_from_db()
        self.assertTrue(hasattr(self.study, "portfolio"))
        self.assertEqual(self.study.portfolio.holdings.count(), 1)

    def test_create_reuses_existing_portfolio(self):
        portfolio = PortfolioFactory(study=self.study)

        response = self.client.post(
            f"/simulations/studies/{self.study.id}/holdings/",
            {
                "ticker": "AAPL",
                "quantity": "10",
                "cost_per_share": "150.00",
                "date_purchased": "2024-01-01",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["portfolio"], portfolio.id)

    def test_create_includes_computed_fields(self):
        response = self.client.post(
            f"/simulations/studies/{self.study.id}/holdings/",
            {
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

    def test_create_on_other_users_study_returns_404(self):
        other_study = StudyFactory(created_by=self.other_user)

        response = self.client.post(
            f"/simulations/studies/{other_study.id}/holdings/",
            {
                "ticker": "AAPL",
                "quantity": "10",
                "cost_per_share": "150.00",
                "date_purchased": "2024-01-01",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_destroy_other_users_holding_returns_404(self):
        other_study = StudyFactory(created_by=self.other_user)
        other_portfolio = PortfolioFactory(study=other_study)
        other_holding = PortfolioHoldingsFactory(portfolio=other_portfolio)

        response = self.client.delete(
            f"/simulations/studies/{other_study.id}/holdings/{other_holding.id}/"
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
