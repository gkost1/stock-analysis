from random import randint

import factory

from simulations.models import PortfolioHoldings

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
            left_digits=randint(1, 6), right_digits=6, positive=True, min_value=1
        )
    )
