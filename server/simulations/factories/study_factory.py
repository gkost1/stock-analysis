import random
from datetime import timedelta

import factory

from simulations.models import Study


class StudyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Study

    start_date = factory.Faker("date_between", start_date="-5y", end_date="-1y")
    end_date = factory.LazyAttribute(
        lambda o: o.start_date + timedelta(days=random.randint(30, 365))
    )
