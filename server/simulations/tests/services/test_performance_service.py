from datetime import date, timedelta
from decimal import Decimal
from unittest import mock

from django.test import SimpleTestCase

from simulations.services.performance_service import PortfolioPerformanceCalculator


class FakeHolding:
    def __init__(self, id, ticker, quantity, cost_per_share, date_purchased, date_sold=None):
        self.id = id
        self.ticker = ticker
        self.quantity = Decimal(quantity)
        self.cost_per_share = Decimal(cost_per_share)
        self.date_purchased = date_purchased
        self.date_sold = date_sold


def flat_price_history(price: Decimal, start: date, end: date) -> dict:
    history = {}
    current = start
    while current <= end:
        history[current] = price
        current += timedelta(days=1)
    return history


PATCH_TARGET = "simulations.services.performance_service.AssetPriceService.get_price_history"


class PortfolioPerformanceCalculatorTests(SimpleTestCase):
    def test_compute_returns_empty_list_when_no_holdings(self):
        calculator = PortfolioPerformanceCalculator([], date(2024, 1, 1), date(2024, 1, 5))

        self.assertEqual(calculator.compute(), [])

    @mock.patch(PATCH_TARGET)
    def test_compute_returns_empty_list_when_holdings_purchased_after_range(
        self, mock_get_price_history
    ):
        holding = FakeHolding(1, "AAPL", "10", "10.00", date(2024, 2, 1))
        calculator = PortfolioPerformanceCalculator([holding], date(2024, 1, 1), date(2024, 1, 5))

        self.assertEqual(calculator.compute(), [])
        mock_get_price_history.assert_not_called()

    @mock.patch(PATCH_TARGET)
    def test_compute_tracks_value_and_profit_loss_across_days(self, mock_get_price_history):
        start, end = date(2024, 1, 1), date(2024, 1, 2)
        mock_get_price_history.return_value = {start: Decimal("10.00"), end: Decimal("12.00")}
        holding = FakeHolding(1, "AAPL", "10", "10.00", start)

        series = PortfolioPerformanceCalculator([holding], start, end).compute()

        self.assertEqual(len(series), 2)
        self.assertEqual(series[0]["date"], start)
        self.assertEqual(series[0]["value"], Decimal("100.00"))
        self.assertEqual(series[0]["profit_loss"], Decimal("0.00"))
        self.assertIsNone(series[0]["cagr"])

        self.assertEqual(series[1]["date"], end)
        self.assertEqual(series[1]["value"], Decimal("120.00"))
        self.assertEqual(series[1]["profit_loss"], Decimal("20.00"))
        self.assertIsNone(series[1]["cagr"])

    @mock.patch(PATCH_TARGET)
    def test_holding_valued_at_cost_basis_before_price_data_exists(self, mock_get_price_history):
        start, end = date(2024, 1, 1), date(2024, 1, 2)
        # No price for the first day (e.g. a non-trading day), only the second.
        mock_get_price_history.return_value = {end: Decimal("12.00")}
        holding = FakeHolding(1, "AAPL", "10", "10.00", start)

        series = PortfolioPerformanceCalculator([holding], start, end).compute()

        self.assertEqual(series[0]["value"], Decimal("100.00"))  # cost basis: 10 * 10.00
        self.assertEqual(series[1]["value"], Decimal("120.00"))  # market price: 10 * 12.00

    @mock.patch(PATCH_TARGET)
    def test_cagr_is_none_before_min_window_and_set_once_reached(self, mock_get_price_history):
        start = date(2024, 1, 1)
        end = start + timedelta(days=PortfolioPerformanceCalculator.MIN_CAGR_WINDOW_DAYS)
        mock_get_price_history.return_value = flat_price_history(Decimal("10.00"), start, end)
        holding = FakeHolding(1, "AAPL", "10", "10.00", start)

        series = PortfolioPerformanceCalculator([holding], start, end).compute()

        for point in series[:-1]:
            self.assertIsNone(point["cagr"])
        # Flat prices mean zero growth, so the CAGR should land on 0 once the window is reached.
        self.assertEqual(series[-1]["cagr"], Decimal("0.0000"))

    @mock.patch(PATCH_TARGET)
    def test_selling_a_holding_is_not_counted_as_a_loss(self, mock_get_price_history):
        start = date(2024, 1, 1)
        sold_date = date(2024, 1, 3)
        end = date(2024, 1, 3)
        mock_get_price_history.return_value = flat_price_history(Decimal("10.00"), start, end)
        holding = FakeHolding(1, "AAPL", "10", "10.00", start, date_sold=sold_date)

        series = PortfolioPerformanceCalculator([holding], start, end).compute()

        # The holding is inactive on its sale date, so the portfolio holds nothing.
        self.assertEqual(series[-1]["value"], Decimal("0"))
        self.assertEqual(series[-1]["profit_loss"], Decimal("0"))
