from decimal import Decimal
from unittest import mock

from django.test import TestCase

from simulations.factories import PortfolioHoldingsFactory


class PortfolioHoldingsPropertiesTests(TestCase):
    def setUp(self):
        patcher = mock.patch(
            "simulations.factories.portfolio_holdings_factory.get_historical_price",
            return_value=Decimal("100.00"),
        )
        patcher.start()
        self.addCleanup(patcher.stop)

    @mock.patch("simulations.models.portfolio_holdings.get_current_price")
    def test_current_share_price_delegates_to_price_service(self, mock_get_current_price):
        mock_get_current_price.return_value = Decimal("200.00")
        holding = PortfolioHoldingsFactory(ticker="AAPL")

        self.assertEqual(holding.current_share_price, Decimal("200.00"))
        mock_get_current_price.assert_called_once_with("AAPL")

    def test_total_cost_is_quantity_times_cost_per_share(self):
        holding = PortfolioHoldingsFactory(quantity=Decimal("10"), cost_per_share=Decimal("15.50"))

        self.assertEqual(holding.total_cost, Decimal("155.00"))

    @mock.patch("simulations.models.portfolio_holdings.get_current_price")
    def test_total_value_uses_current_price(self, mock_get_current_price):
        mock_get_current_price.return_value = Decimal("20.00")
        holding = PortfolioHoldingsFactory(quantity=Decimal("10"), cost_per_share=Decimal("15.00"))

        self.assertEqual(holding.total_value, Decimal("200.00"))

    @mock.patch("simulations.models.portfolio_holdings.get_current_price")
    def test_total_value_is_none_when_price_unavailable(self, mock_get_current_price):
        mock_get_current_price.return_value = None
        holding = PortfolioHoldingsFactory()

        self.assertIsNone(holding.total_value)

    @mock.patch("simulations.models.portfolio_holdings.get_current_price")
    def test_profit_loss_is_total_value_minus_total_cost(self, mock_get_current_price):
        mock_get_current_price.return_value = Decimal("20.00")
        holding = PortfolioHoldingsFactory(quantity=Decimal("10"), cost_per_share=Decimal("15.00"))

        self.assertEqual(holding.profit_loss, Decimal("50.00"))

    @mock.patch("simulations.models.portfolio_holdings.get_current_price")
    def test_profit_loss_is_none_when_price_unavailable(self, mock_get_current_price):
        mock_get_current_price.return_value = None
        holding = PortfolioHoldingsFactory()

        self.assertIsNone(holding.profit_loss)
