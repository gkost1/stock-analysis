from datetime import date, timedelta
from decimal import Decimal

import yfinance as yf
from django.utils import timezone

from simulations.models import CachedTickerPrice


class AssetPriceService:
    CURRENT_PRICE_CACHE_TTL = timedelta(minutes=60)

    @staticmethod
    def _is_expired(cached: CachedTickerPrice):
        return timezone.now() - cached.updated_at > AssetPriceService.CURRENT_PRICE_CACHE_TTL

    @staticmethod
    def get_current_price(ticker: str) -> Decimal | None:

        cached = CachedTickerPrice.objects.filter(ticker=ticker).first()
        if cached and not AssetPriceService._is_expired(cached):
            return cached.price

        price = yf.Ticker(ticker).fast_info.get("lastPrice")
        price = Decimal(str(price)) if price is not None else None

        CachedTickerPrice.objects.update_or_create(ticker=ticker, defaults={"price": price})

        return price

    @staticmethod
    def get_historical_price(ticker: str, on_date: date) -> Decimal | None:
        history = yf.Ticker(ticker).history(start=on_date, end=on_date + timedelta(days=7))
        if history.empty:
            return None
        return Decimal(str(history["Close"].iloc[0]))

    @staticmethod
    def get_price_history(ticker: str, start_date: date, end_date: date) -> dict[date, Decimal]:
        history = yf.Ticker(ticker).history(start=start_date, end=end_date + timedelta(days=1))
        return {
            timestamp.date(): Decimal(str(close)) for timestamp, close in history["Close"].items()
        }
