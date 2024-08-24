"""
Django command to wait for the database to be available.
"""

import time
from typing import Any

from psycopg2 import OperationalError as PsyOperationalError

from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


WAIT_TIME = 1


class Command(BaseCommand):
    """Django command to wait for database."""

    def handle(self, *args: Any, **options: Any):
        """Entrypoint for the command."""

        self.stdout.write("Waiting for database...")
        db_up = False
        while not db_up:
            try:
                self.check(databases=["default"])
                db_up = True
            except (PsyOperationalError, OperationalError):
                self.stdout.write(
                    f"Database unavailable, \
                    waiting for [{WAIT_TIME}]s"
                )
                time.sleep(WAIT_TIME)

        self.stdout.write(self.style.SUCCESS("Database Available!"))
