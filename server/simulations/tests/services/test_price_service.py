from datetime import date
from decimal import Decimal
from unittest import mock

import pandas as pd
from django.test import TestCase

from simulations.services import price_service


class GetCurrentPriceTests(TestCase):
    @mock.patch("simulations.services.price_service.yf.Ticker")
    def test_returns_decimal_price(self, mock_ticker):
        mock_ticker.return_value.fast_info = {"lastPrice": 123.45}

        price = price_service.get_current_price("AAPL")

        self.assertEqual(price, Decimal("123.45"))
        mock_ticker.assert_called_once_with("AAPL")

    @mock.patch("simulations.services.price_service.yf.Ticker")
    def test_returns_none_when_price_missing(self, mock_ticker):
        mock_ticker.return_value.fast_info = {}

        price = price_service.get_current_price("AAPL")

        self.assertIsNone(price)


class GetHistoricalPriceTests(TestCase):
    @mock.patch("simulations.services.price_service.yf.Ticker")
    def test_returns_first_close_price(self, mock_ticker):
        mock_ticker.return_value.history.return_value = pd.DataFrame({"Close": [150.25, 151.0]})

        price = price_service.get_historical_price("AAPL", date(2024, 1, 1))

        self.assertEqual(price, Decimal("150.25"))
        mock_ticker.return_value.history.assert_called_once_with(
            start=date(2024, 1, 1), end=date(2024, 1, 8)
        )

    @mock.patch("simulations.services.price_service.yf.Ticker")
    def test_returns_none_when_history_empty(self, mock_ticker):
        mock_ticker.return_value.history.return_value = pd.DataFrame()

        price = price_service.get_historical_price("AAPL", date(2024, 1, 1))

        self.assertIsNone(price)
