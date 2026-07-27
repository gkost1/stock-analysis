import psycopg
from psycopg import sql

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import connections, transaction

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
        self.stdout.write("Dropping and recreating the database...")
        self._recreate_database()

        self.stdout.write("Applying migrations...")
        call_command("migrate", interactive=False, verbosity=0)

        with transaction.atomic():
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

    def _recreate_database(self):
        db_settings = settings.DATABASES["default"]
        db_name = db_settings["NAME"]

        connections.close_all()

        conn = psycopg.connect(
            dbname="postgres",
            user=db_settings["USER"],
            password=db_settings["PASSWORD"],
            host=db_settings["HOST"],
            port=db_settings["PORT"],
            autocommit=True,
        )
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    sql.SQL("DROP DATABASE IF EXISTS {} WITH (FORCE)").format(
                        sql.Identifier(db_name)
                    )
                )
                cursor.execute(
                    sql.SQL("CREATE DATABASE {} OWNER {}").format(
                        sql.Identifier(db_name), sql.Identifier(db_settings["USER"])
                    )
                )
        finally:
            conn.close()
