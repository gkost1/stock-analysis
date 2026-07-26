from random import randint

import factory

from simulations.models import Portfolio

from .faker import fake


class PortfolioFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Portfolio

    initial_investment = factory.LazyFunction(
        lambda: fake.pydecimal(
            left_digits=randint(4, 6), right_digits=2, positive=True, min_value=1000
        )
    )
