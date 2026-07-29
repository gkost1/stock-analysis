from datetime import date
from decimal import Decimal
from unittest import mock

from django.test import TestCase

from simulations.factories import PortfolioFactory, PortfolioHoldingsFactory
from simulations.models import PortfolioHoldings


class PortfolioHoldingsPropertiesTests(TestCase):
    def setUp(self):
        patcher = mock.patch(
            "simulations.factories.portfolio_holdings_factory.AssetPriceService.get_historical_price",
            return_value=Decimal("100.00"),
        )
        patcher.start()
        self.addCleanup(patcher.stop)

    @mock.patch("simulations.models.portfolio_holdings.AssetPriceService.get_current_price")
    def test_current_share_price_delegates_to_price_service(self, mock_get_current_price):
        mock_get_current_price.return_value = Decimal("200.00")
        holding = PortfolioHoldingsFactory(ticker="AAPL")

        self.assertEqual(holding.current_share_price, Decimal("200.00"))
        mock_get_current_price.assert_called_once_with("AAPL")

    def test_total_cost_is_quantity_times_cost_per_share(self):
        holding = PortfolioHoldingsFactory(quantity=Decimal("10"), cost_per_share=Decimal("15.50"))

        self.assertEqual(holding.total_cost, Decimal("155.00"))

    @mock.patch("simulations.models.portfolio_holdings.AssetPriceService.get_current_price")
    def test_total_value_uses_current_price(self, mock_get_current_price):
        mock_get_current_price.return_value = Decimal("20.00")
        holding = PortfolioHoldingsFactory(quantity=Decimal("10"), cost_per_share=Decimal("15.00"))

        self.assertEqual(holding.total_value, Decimal("200.00"))

    @mock.patch("simulations.models.portfolio_holdings.AssetPriceService.get_current_price")
    def test_total_value_is_none_when_price_unavailable(self, mock_get_current_price):
        mock_get_current_price.return_value = None
        holding = PortfolioHoldingsFactory()

        self.assertIsNone(holding.total_value)

    @mock.patch("simulations.models.portfolio_holdings.AssetPriceService.get_current_price")
    def test_profit_loss_is_total_value_minus_total_cost(self, mock_get_current_price):
        mock_get_current_price.return_value = Decimal("20.00")
        holding = PortfolioHoldingsFactory(quantity=Decimal("10"), cost_per_share=Decimal("15.00"))

        self.assertEqual(holding.profit_loss, Decimal("50.00"))

    @mock.patch("simulations.models.portfolio_holdings.AssetPriceService.get_current_price")
    def test_profit_loss_is_none_when_price_unavailable(self, mock_get_current_price):
        mock_get_current_price.return_value = None
        holding = PortfolioHoldingsFactory()

        self.assertIsNone(holding.profit_loss)


class ConsolidateByTickerTests(TestCase):
    def setUp(self):
        patcher = mock.patch(
            "simulations.factories.portfolio_holdings_factory.AssetPriceService.get_historical_price",
            return_value=Decimal("100.00"),
        )
        patcher.start()
        self.addCleanup(patcher.stop)

        self.portfolio = PortfolioFactory()

    def test_groups_holdings_by_ticker(self):
        PortfolioHoldingsFactory(portfolio=self.portfolio, ticker="AAPL")
        PortfolioHoldingsFactory(portfolio=self.portfolio, ticker="AAPL")
        PortfolioHoldingsFactory(portfolio=self.portfolio, ticker="MSFT")

        consolidated = PortfolioHoldings.consolidate_by_ticker(
            PortfolioHoldings.objects.filter(portfolio=self.portfolio)
        )

        tickers = sorted(row.ticker for row in consolidated)
        self.assertEqual(tickers, ["AAPL", "MSFT"])

    def test_single_lot_reports_its_own_values(self):
        holding = PortfolioHoldingsFactory(
            portfolio=self.portfolio,
            ticker="AAPL",
            quantity=Decimal("10"),
            cost_per_share=Decimal("15.00"),
            date_purchased=date(2024, 1, 1),
        )

        [consolidated] = PortfolioHoldings.consolidate_by_ticker([holding])

        self.assertEqual(consolidated.id, holding.id)
        self.assertEqual(consolidated.portfolio, self.portfolio.id)
        self.assertEqual(consolidated.quantity, Decimal("10"))
        self.assertEqual(consolidated.cost_per_share, Decimal("15.00"))
        self.assertEqual(consolidated.date_purchased, "2024-01-01")
        self.assertIsNone(consolidated.date_sold)

    def test_multiple_lots_sum_quantity_and_average_cost(self):
        first = PortfolioHoldingsFactory(
            portfolio=self.portfolio,
            ticker="AAPL",
            quantity=Decimal("10"),
            cost_per_share=Decimal("10.00"),
            date_purchased=date(2024, 1, 1),
        )
        second = PortfolioHoldingsFactory(
            portfolio=self.portfolio,
            ticker="AAPL",
            quantity=Decimal("30"),
            cost_per_share=Decimal("20.00"),
            date_purchased=date(2024, 2, 1),
        )

        [consolidated] = PortfolioHoldings.consolidate_by_ticker([first, second])

        self.assertEqual(consolidated.quantity, Decimal("40"))
        self.assertEqual(consolidated.total_cost, Decimal("700.00"))
        self.assertEqual(consolidated.cost_per_share, Decimal("17.5"))
        self.assertEqual(consolidated.date_purchased, "varies")

    @mock.patch("simulations.models.portfolio_holdings.AssetPriceService.get_current_price")
    def test_current_share_price_uses_first_available_price_across_lots(
        self, mock_get_current_price
    ):
        mock_get_current_price.return_value = Decimal("25.00")
        first = PortfolioHoldingsFactory(portfolio=self.portfolio, ticker="AAPL")
        second = PortfolioHoldingsFactory(portfolio=self.portfolio, ticker="AAPL")

        [consolidated] = PortfolioHoldings.consolidate_by_ticker([first, second])

        self.assertEqual(consolidated.current_share_price, Decimal("25.00"))

    @mock.patch("simulations.models.portfolio_holdings.AssetPriceService.get_current_price")
    def test_total_value_and_profit_loss_sum_across_lots(self, mock_get_current_price):
        mock_get_current_price.return_value = Decimal("20.00")
        first = PortfolioHoldingsFactory(
            portfolio=self.portfolio,
            ticker="AAPL",
            quantity=Decimal("10"),
            cost_per_share=Decimal("10.00"),
        )
        second = PortfolioHoldingsFactory(
            portfolio=self.portfolio,
            ticker="AAPL",
            quantity=Decimal("5"),
            cost_per_share=Decimal("10.00"),
        )

        [consolidated] = PortfolioHoldings.consolidate_by_ticker([first, second])

        self.assertEqual(consolidated.total_value, Decimal("300.00"))
        self.assertEqual(consolidated.profit_loss, Decimal("150.00"))

    @mock.patch("simulations.models.portfolio_holdings.AssetPriceService.get_current_price")
    def test_total_value_is_none_when_any_lot_price_unavailable(self, mock_get_current_price):
        mock_get_current_price.return_value = None
        first = PortfolioHoldingsFactory(portfolio=self.portfolio, ticker="AAPL")
        second = PortfolioHoldingsFactory(portfolio=self.portfolio, ticker="AAPL")

        [consolidated] = PortfolioHoldings.consolidate_by_ticker([first, second])

        self.assertIsNone(consolidated.total_value)
        self.assertIsNone(consolidated.profit_loss)
