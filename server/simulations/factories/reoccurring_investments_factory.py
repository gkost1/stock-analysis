from random import randint

import factory

from simulations.models import ReoccurringInvestments
from simulations.models.reocurring_investments import INVESTMENT_FREQUENCY_CHOICES

from .faker import fake
from .portfolio_factory import PortfolioFactory
from .portfolio_holdings_factory import TICKERS


class ReoccurringInvestmentsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ReoccurringInvestments

    portfolio = factory.SubFactory(PortfolioFactory)
    frequency = factory.Faker(
        "random_element", elements=[choice[0] for choice in INVESTMENT_FREQUENCY_CHOICES]
    )
    ticker = factory.Faker("random_element", elements=TICKERS)
    dollar_amount = factory.LazyFunction(
        lambda: fake.pydecimal(
            left_digits=randint(3, 6), right_digits=2, positive=True, min_value=100
        )
    )
    start_date = factory.Faker("date_between", start_date="-2y", end_date="today")
    end_date = None
