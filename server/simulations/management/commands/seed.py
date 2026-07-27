from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import transaction

from core.factories import UserFactory
from simulations.factories import (
    PortfolioFactory,
    PortfolioHoldingsFactory,
    PortfolioTransactionsFactory,
    RecurringInvestmentsFactory,
    StudyFactory,
)


class Command(BaseCommand):
    help = "Drop and recreate the database, then seed it with fake data using the model factories."

    def add_arguments(self, parser):
        parser.add_argument("--studies", type=int, default=5)
        parser.add_argument("--portfolios", type=int, default=10)
        parser.add_argument("--holdings-per-portfolio", type=int, default=4)
        parser.add_argument("--transactions-per-portfolio", type=int, default=10)
        parser.add_argument("--recurring-per-portfolio", type=int, default=2)

    def handle(self, *args, **options):
        call_command("resetdb")

        with transaction.atomic():
            user = UserFactory()
            StudyFactory.create_batch(options["studies"], created_by=user)

            for _ in range(options["portfolios"]):
                portfolio = PortfolioFactory()

                for _ in range(options["holdings_per_portfolio"]):
                    PortfolioHoldingsFactory(portfolio=portfolio)
                for _ in range(options["transactions_per_portfolio"]):
                    PortfolioTransactionsFactory(portfolio=portfolio)
                for _ in range(options["transactions_per_portfolio"]):
                    RecurringInvestmentsFactory(portfolio=portfolio)

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded {options['studies']} studies and {options['portfolios']} portfolios."
            )
        )
