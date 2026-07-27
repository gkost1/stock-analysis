import random
from datetime import timedelta

import factory

from core.factories import UserFactory
from simulations.models import Study

from .faker import fake


class StudyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Study

    created_by = factory.SubFactory(UserFactory)
    title = factory.LazyFunction(
        lambda: fake.sentence(nb_words=random.randint(1, 4), variable_nb_words=False).rstrip(".")
    )
    start_date = factory.Faker("date_between", start_date="-5y", end_date="-1y")
    end_date = factory.LazyAttribute(
        lambda o: o.start_date + timedelta(days=random.randint(30, 365))
    )
