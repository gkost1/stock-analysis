import random
from datetime import timedelta
from random import randint

import factory

from core.factories import UserFactory
from simulations.models import Portfolio

from .faker import fake


class PortfolioFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Portfolio

    created_by = factory.SubFactory(UserFactory)
    title = factory.LazyFunction(
        lambda: fake.sentence(nb_words=random.randint(1, 4), variable_nb_words=False).rstrip(".")
    )
    start_date = factory.Faker("date_between", start_date="-5y", end_date="-1y")
    end_date = factory.LazyAttribute(
        lambda o: o.start_date + timedelta(days=random.randint(30, 365))
    )
    initial_investment = factory.LazyFunction(
        lambda: fake.pydecimal(
            left_digits=randint(4, 6), right_digits=2, positive=True, min_value=1000
        )
    )
