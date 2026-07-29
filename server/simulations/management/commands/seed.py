import random

from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import transaction

from core.factories import UserFactory
from simulations.factories import (
    PortfolioFactory,
    PortfolioHoldingsFactory,
    PortfolioTransactionsFactory,
    RecurringInvestmentsFactory,
)


class Command(BaseCommand):
    help = "Drop and recreate the database, then seed it with fake data using the model factories."

    def add_arguments(self, parser):
        parser.add_argument("--portfolios", type=int, default=5)
        parser.add_argument("--min-holdings-per-portfolio", type=int, default=5)
        parser.add_argument("--max-holdings-per-portfolio", type=int, default=20)
        parser.add_argument("--transactions-per-portfolio", type=int, default=10)
        parser.add_argument("--recurring-per-portfolio", type=int, default=2)

    def handle(self, *args, **options):
        call_command("resetdb")

        with transaction.atomic():
            user = UserFactory()
            portfolios = PortfolioFactory.create_batch(options["portfolios"], created_by=user)

            for portfolio in portfolios:
                holdings_count = random.randint(
                    options["min_holdings_per_portfolio"], options["max_holdings_per_portfolio"]
                )
                for _ in range(holdings_count):
                    PortfolioHoldingsFactory(portfolio=portfolio)
                for _ in range(options["transactions_per_portfolio"]):
                    PortfolioTransactionsFactory(portfolio=portfolio)
                for _ in range(options["recurring_per_portfolio"]):
                    RecurringInvestmentsFactory(portfolio=portfolio)

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded {options['portfolios']} portfolios, each with 5-20 holdings."
            )
        )
