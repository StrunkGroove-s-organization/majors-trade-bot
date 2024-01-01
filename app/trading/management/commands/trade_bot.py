import time
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Run the trading bot indefinitely'

    def handle(self, *args, **options):
        while True:
            time.sleep(60)