import math
from datetime import date, timedelta
from decimal import Decimal

from .price_service import AssetPriceService


class PortfolioPerformanceCalculator:
    MIN_CAGR_WINDOW_DAYS = 30

    def __init__(self, holdings, start_date: date, end_date: date):
        self.holdings = list(holdings)
        self.start_date = start_date
        self.end_date = end_date

        self._last_known_prices: dict[str, Decimal | None] = {}
        self._price_histories: dict[str, dict[date, Decimal]] = {}

    @property
    def range_start(self) -> date | None:
        if not self.holdings:
            return None
        return max(self.start_date, min(holding.date_purchased for holding in self.holdings))

    @property
    def range_end(self) -> date:
        return min(self.end_date, date.today())

    def compute(self) -> list[dict]:
        if not self.holdings or self.range_start > self.range_end:
            return []

        tickers = {holding.ticker for holding in self.holdings}
        self._price_histories = {
            ticker: AssetPriceService.get_price_history(ticker, self.range_start, self.range_end)
            for ticker in tickers
        }
        self._last_known_prices = dict.fromkeys(tickers)

        # Time-weighted return: contributions (new holdings) and withdrawals (sold
        # holdings) are treated as neutral cash flows, not gains/losses, so a large
        # purchase mid-timeline doesn't distort the annualized growth rate.
        prev_values: dict[int, Decimal] = {}
        prev_total_value = Decimal("0")
        cumulative_growth = Decimal("1")

        series = []
        current_date = self.range_start
        while current_date <= self.range_end:
            active_holdings = self._active_holdings(current_date)
            today_values = {
                holding_id: self._holding_value(holding, current_date)
                for holding_id, holding in active_holdings.items()
            }
            total_value = sum(today_values.values(), Decimal("0"))
            total_cost = self._total_cost(active_holdings)

            contribution = self._net_contribution(active_holdings, prev_values)
            baseline = prev_total_value + contribution
            if baseline > 0:
                cumulative_growth *= total_value / baseline

            days_elapsed = (current_date - self.range_start).days
            cagr = self._cagr(cumulative_growth, days_elapsed)

            series.append(
                {
                    "date": current_date,
                    "value": total_value,
                    "profit_loss": total_value - total_cost,
                    "cagr": cagr,
                }
            )

            prev_values = today_values
            prev_total_value = total_value
            current_date += timedelta(days=1)

        return series

    def _active_holdings(self, current_date: date) -> dict[int, object]:
        return {
            holding.id: holding
            for holding in self.holdings
            if holding.date_purchased <= current_date
            and (holding.date_sold is None or holding.date_sold > current_date)
        }

    @staticmethod
    def _total_cost(active_holdings: dict[int, object]) -> Decimal:
        return sum(
            (holding.cost_per_share * holding.quantity for holding in active_holdings.values()),
            Decimal("0"),
        )

    @staticmethod
    def _net_contribution(
        active_holdings: dict[int, object], prev_values: dict[int, Decimal]
    ) -> Decimal:
        new_entrants = active_holdings.keys() - prev_values.keys()
        departed = prev_values.keys() - active_holdings.keys()
        inflows = sum(
            (
                active_holdings[holding_id].cost_per_share * active_holdings[holding_id].quantity
                for holding_id in new_entrants
            ),
            Decimal("0"),
        )
        outflows = sum((prev_values[holding_id] for holding_id in departed), Decimal("0"))
        return inflows - outflows

    def _holding_value(self, holding, current_date: date) -> Decimal:
        price = self._price_histories[holding.ticker].get(current_date)
        if price is not None:
            self._last_known_prices[holding.ticker] = price
        price = self._last_known_prices[holding.ticker]

        # Before the first available market price, value the holding at its cost
        # basis (what was actually invested) rather than 0.
        return (
            price * holding.quantity
            if price is not None
            else holding.cost_per_share * holding.quantity
        )

    def _cagr(self, cumulative_growth: Decimal, days_elapsed: int) -> Decimal | None:
        if days_elapsed < self.MIN_CAGR_WINDOW_DAYS:
            return None

        years = Decimal(days_elapsed) / Decimal("365.25")
        return self._compute_cagr(cumulative_growth, years)

    @staticmethod
    def _compute_cagr(cumulative_growth: Decimal, years: Decimal) -> Decimal | None:
        if cumulative_growth <= 0 or years <= 0:
            return None

        try:
            result = float(cumulative_growth) ** (1 / float(years)) - 1
        except (OverflowError, ValueError, ZeroDivisionError):
            return None

        if not math.isfinite(result):
            return None

        return Decimal(str(round(result, 4)))
