from random import randint

import factory

from simulations.models import Portfolio

from .faker import fake
from .study_factory import StudyFactory


class PortfolioFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Portfolio

    study = factory.SubFactory(StudyFactory)
    initial_investment = factory.LazyFunction(
        lambda: fake.pydecimal(
            left_digits=randint(4, 6), right_digits=2, positive=True, min_value=1000
        )
    )
