import time

from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError


class Command(BaseCommand):
    """
    Waits for the database to become available before continuing.
    Useful in Docker Compose, where the 'db' container may take a
    few seconds after starting before it actually accepts connections.
    """
    help = 'Wait for the database to be available'

    def handle(self, *args, **options):
        self.stdout.write('Checking database connection...')
        db_conn = None
        attempts = 0
        max_attempts = 30
        while not db_conn and attempts < max_attempts:
            try:
                connections['default'].cursor()
                db_conn = True
            except OperationalError:
                attempts += 1
                self.stdout.write(f'Database unavailable, waiting 1 second... ({attempts}/{max_attempts})')
                time.sleep(1)

        if not db_conn:
            self.stderr.write(self.style.ERROR('Database never became available.'))
            raise SystemExit(1)

        self.stdout.write(self.style.SUCCESS('Database available!'))
