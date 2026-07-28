from datetime import date, timedelta
from decimal import Decimal

import yfinance as yf


def get_current_price(ticker: str) -> Decimal | None:
    price = yf.Ticker(ticker).fast_info.get("lastPrice")
    return Decimal(str(price)) if price is not None else None


def get_historical_price(ticker: str, on_date: date) -> Decimal | None:
    history = yf.Ticker(ticker).history(start=on_date, end=on_date + timedelta(days=7))
    if history.empty:
        return None
    return Decimal(str(history["Close"].iloc[0]))


def get_price_history(ticker: str, start_date: date, end_date: date) -> dict[date, Decimal]:
    history = yf.Ticker(ticker).history(start=start_date, end=end_date + timedelta(days=1))
    return {timestamp.date(): Decimal(str(close)) for timestamp, close in history["Close"].items()}
