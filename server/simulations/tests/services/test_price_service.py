from datetime import date, timedelta
from decimal import Decimal
from unittest import mock

import pandas as pd
from django.test import TestCase
from django.utils import timezone

from simulations.models import CachedTickerPrice
from simulations.services import price_service


class GetCurrentPriceTests(TestCase):
    @mock.patch("simulations.services.price_service.yf.Ticker")
    def test_returns_decimal_price(self, mock_ticker):
        mock_ticker.return_value.fast_info = {"lastPrice": 123.45}

        price = price_service.AssetPriceService.get_current_price("AAPL")

        self.assertEqual(price, Decimal("123.45"))
        mock_ticker.assert_called_once_with("AAPL")

    @mock.patch("simulations.services.price_service.yf.Ticker")
    def test_returns_none_when_price_missing(self, mock_ticker):
        mock_ticker.return_value.fast_info = {}

        price = price_service.AssetPriceService.get_current_price("AAPL")

        self.assertIsNone(price)

    @mock.patch("simulations.services.price_service.yf.Ticker")
    def test_caches_price_after_fetch(self, mock_ticker):
        mock_ticker.return_value.fast_info = {"lastPrice": 123.45}

        price_service.AssetPriceService.get_current_price("AAPL")

        cached = CachedTickerPrice.objects.get(ticker="AAPL")
        self.assertEqual(cached.price, Decimal("123.45"))

    @mock.patch("simulations.services.price_service.yf.Ticker")
    def test_uses_cached_price_within_ttl_without_hitting_yfinance(self, mock_ticker):
        CachedTickerPrice.objects.create(ticker="AAPL", price=Decimal("100.00"))

        price = price_service.AssetPriceService.get_current_price("AAPL")

        self.assertEqual(price, Decimal("100.00"))
        mock_ticker.assert_not_called()

    @mock.patch("simulations.services.price_service.yf.Ticker")
    def test_refetches_when_cache_is_older_than_ttl(self, mock_ticker):
        mock_ticker.return_value.fast_info = {"lastPrice": 200.00}
        cached = CachedTickerPrice.objects.create(ticker="AAPL", price=Decimal("100.00"))
        stale_time = timezone.now() - price_service.AssetPriceService.CURRENT_PRICE_CACHE_TTL
        stale_time -= timedelta(seconds=1)
        CachedTickerPrice.objects.filter(pk=cached.pk).update(updated_at=stale_time)

        price = price_service.AssetPriceService.get_current_price("AAPL")

        self.assertEqual(price, Decimal("200.00"))
        mock_ticker.assert_called_once_with("AAPL")

    @mock.patch("simulations.services.price_service.yf.Ticker")
    def test_refetch_updates_existing_cache_row_instead_of_duplicating(self, mock_ticker):
        mock_ticker.return_value.fast_info = {"lastPrice": 200.00}
        cached = CachedTickerPrice.objects.create(ticker="AAPL", price=Decimal("100.00"))
        stale_time = timezone.now() - price_service.AssetPriceService.CURRENT_PRICE_CACHE_TTL
        stale_time -= timedelta(seconds=1)
        CachedTickerPrice.objects.filter(pk=cached.pk).update(updated_at=stale_time)

        price_service.AssetPriceService.get_current_price("AAPL")

        self.assertEqual(CachedTickerPrice.objects.filter(ticker="AAPL").count(), 1)
        cached.refresh_from_db()
        self.assertEqual(cached.price, Decimal("200.00"))

    @mock.patch("simulations.services.price_service.yf.Ticker")
    def test_different_tickers_are_cached_independently(self, mock_ticker):
        mock_ticker.return_value.fast_info = {"lastPrice": 55.00}
        CachedTickerPrice.objects.create(ticker="AAPL", price=Decimal("100.00"))

        price = price_service.AssetPriceService.get_current_price("MSFT")

        self.assertEqual(price, Decimal("55.00"))
        mock_ticker.assert_called_once_with("MSFT")


class GetHistoricalPriceTests(TestCase):
    @mock.patch("simulations.services.price_service.yf.Ticker")
    def test_returns_first_close_price(self, mock_ticker):
        mock_ticker.return_value.history.return_value = pd.DataFrame({"Close": [150.25, 151.0]})

        price = price_service.AssetPriceService.get_historical_price("AAPL", date(2024, 1, 1))

        self.assertEqual(price, Decimal("150.25"))
        mock_ticker.return_value.history.assert_called_once_with(
            start=date(2024, 1, 1), end=date(2024, 1, 8)
        )

    @mock.patch("simulations.services.price_service.yf.Ticker")
    def test_returns_none_when_history_empty(self, mock_ticker):
        mock_ticker.return_value.history.return_value = pd.DataFrame()

        price = price_service.AssetPriceService.get_historical_price("AAPL", date(2024, 1, 1))

        self.assertIsNone(price)


class GetPriceHistoryTests(TestCase):
    @mock.patch("simulations.services.price_service.yf.Ticker")
    def test_returns_close_price_keyed_by_date(self, mock_ticker):
        mock_ticker.return_value.history.return_value = pd.DataFrame(
            {"Close": [150.25, 151.50]},
            index=pd.to_datetime(["2024-01-01", "2024-01-02"]),
        )

        history = price_service.AssetPriceService.get_price_history(
            "AAPL", date(2024, 1, 1), date(2024, 1, 2)
        )

        self.assertEqual(
            history,
            {
                date(2024, 1, 1): Decimal("150.25"),
                date(2024, 1, 2): Decimal("151.50"),
            },
        )
        mock_ticker.return_value.history.assert_called_once_with(
            start=date(2024, 1, 1), end=date(2024, 1, 3)
        )

    @mock.patch("simulations.services.price_service.yf.Ticker")
    def test_returns_empty_dict_when_no_history(self, mock_ticker):
        mock_ticker.return_value.history.return_value = pd.DataFrame({"Close": []})

        history = price_service.AssetPriceService.get_price_history(
            "AAPL", date(2024, 1, 1), date(2024, 1, 2)
        )

        self.assertEqual(history, {})
