from random import randint

import factory

from simulations.models import PortfolioHoldings
from simulations.services import AssetPriceService

from .faker import fake
from .portfolio_factory import PortfolioFactory

TICKERS = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "TSLA", "META", "SPY"]


class PortfolioHoldingsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PortfolioHoldings

    portfolio = factory.SubFactory(PortfolioFactory)
    ticker = factory.Faker("random_element", elements=TICKERS)
    quantity = factory.LazyFunction(
        lambda: fake.pydecimal(
            left_digits=randint(1, 3), right_digits=6, positive=True, min_value=1
        )
    )
    date_purchased = factory.Faker("date_between", start_date="-3y", end_date="-1y")
    date_sold = None
    cost_per_share = factory.LazyAttribute(
        lambda o: (
            AssetPriceService.get_historical_price(o.ticker, o.date_purchased)
            or fake.pydecimal(left_digits=randint(1, 3), right_digits=2, positive=True, min_value=1)
        )
    )
