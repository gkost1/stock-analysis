import psycopg
from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import connections
from psycopg import sql


class Command(BaseCommand):
    help = "Drop and recreate the configured database, then apply migrations."

    def handle(self, *args, **options):
        db_name = settings.DATABASES["default"]["NAME"]
        self.stdout.write(f"Dropping and recreating database {db_name!r}...")
        self._recreate_database()

        self.stdout.write("Applying migrations...")
        call_command("migrate", interactive=False, verbosity=0)

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
