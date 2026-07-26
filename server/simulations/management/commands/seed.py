from django.core.management.base import BaseCommand
from django.db import transaction

from simulations.factories import (
    PortfolioFactory,
    PortfolioHoldingsFactory,
    PortfolioTransactionsFactory,
    RecurringInvestmentsFactory,
    StudyFactory,
)
from simulations.models import (
    Portfolio,
    PortfolioHoldings,
    PortfolioTransactions,
    RecurringInvestments,
    Study,
)


class Command(BaseCommand):
    help = "Seed the simulations app with fake data using the model factories."

    def add_arguments(self, parser):
        parser.add_argument("--studies", type=int, default=5)
        parser.add_argument("--portfolios", type=int, default=10)
        parser.add_argument("--holdings-per-portfolio", type=int, default=4)
        parser.add_argument("--transactions-per-portfolio", type=int, default=10)
        parser.add_argument("--recurring-per-portfolio", type=int, default=2)
        parser.add_argument(
            "--flush",
            action="store_true",
            help="Delete existing simulations data before seeding.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if options["flush"]:
            self.stdout.write("Flushing existing simulations data...")
            PortfolioTransactions.objects.all().delete()
            PortfolioHoldings.objects.all().delete()
            RecurringInvestments.objects.all().delete()
            Portfolio.objects.all().delete()
            Study.objects.all().delete()

        StudyFactory.create_batch(options["studies"])

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
