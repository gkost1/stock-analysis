from rest_framework import status
from rest_framework.test import APITestCase

from core.factories import UserFactory
from simulations.factories import PortfolioFactory


class PortfolioViewSetTests(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.other_user = UserFactory()
        self.client.force_authenticate(user=self.user)

    def test_list_only_returns_own_portfolios(self):
        own_portfolio = PortfolioFactory(created_by=self.user)
        PortfolioFactory(created_by=self.other_user)

        response = self.client.get("/simulations/portfolios/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ids = [portfolio["id"] for portfolio in response.data]
        self.assertEqual(ids, [own_portfolio.id])

    def test_retrieve_own_portfolio_returns_200(self):
        own_portfolio = PortfolioFactory(created_by=self.user)

        response = self.client.get(f"/simulations/portfolios/{own_portfolio.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], own_portfolio.id)

    def test_retrieve_other_users_portfolio_returns_404(self):
        other_portfolio = PortfolioFactory(created_by=self.other_user)

        response = self.client.get(f"/simulations/portfolios/{other_portfolio.id}/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_other_users_portfolio_returns_404(self):
        other_portfolio = PortfolioFactory(created_by=self.other_user)

        response = self.client.patch(
            f"/simulations/portfolios/{other_portfolio.id}/", {"title": "Hijacked"}
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_destroy_other_users_portfolio_returns_404(self):
        other_portfolio = PortfolioFactory(created_by=self.other_user)

        response = self.client.delete(f"/simulations/portfolios/{other_portfolio.id}/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
