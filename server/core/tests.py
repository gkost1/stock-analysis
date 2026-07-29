from django.test import override_settings
from rest_framework import status
from rest_framework.test import APITestCase

from core.factories import UserFactory
from simulations.models import Portfolio


class SeedViewTests(APITestCase):
    @override_settings(DEBUG=True)
    def test_creates_instance_via_named_factory(self):
        user = UserFactory()

        response = self.client.post(
            "/core/testing/seed/",
            {
                "factory": "PortfolioFactory",
                "attrs": {
                    "created_by_id": user.id,
                    "title": "Seeded Portfolio",
                    "start_date": "2024-01-01",
                    "end_date": "2024-06-01",
                },
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        portfolio = Portfolio.objects.get(pk=response.data["id"])
        self.assertEqual(portfolio.title, "Seeded Portfolio")
        self.assertEqual(portfolio.created_by, user)

    @override_settings(DEBUG=True)
    def test_unknown_factory_returns_400(self):
        response = self.client.post(
            "/core/testing/seed/",
            {"factory": "NotARealFactory", "attrs": {}},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @override_settings(DEBUG=False)
    def test_disabled_outside_debug(self):
        response = self.client.post(
            "/core/testing/seed/",
            {"factory": "PortfolioFactory", "attrs": {}},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
