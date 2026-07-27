from random import randint

import factory

from simulations.models import PortfolioTransactions
from simulations.models.portfolio_transactions import TRANSACTION_TYPE_CHOICES

from .faker import fake
from .portfolio_factory import PortfolioFactory
from .portfolio_holdings_factory import TICKERS


class PortfolioTransactionsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PortfolioTransactions

    portfolio = factory.SubFactory(PortfolioFactory)
    type = factory.Faker(
        "random_element", elements=[choice[0] for choice in TRANSACTION_TYPE_CHOICES]
    )
    ticker = factory.Faker("random_element", elements=TICKERS)
    price = factory.LazyFunction(
        lambda: fake.pydecimal(
            left_digits=randint(1, 4), right_digits=2, positive=True, min_value=1
        )
    )
    quantity = factory.LazyFunction(
        lambda: fake.pydecimal(
            left_digits=randint(1, 6), right_digits=6, positive=True, min_value=1
        )
    )
    date = factory.Faker("date_between", start_date="-2y", end_date="today")
