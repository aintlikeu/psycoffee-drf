from django.core.management.base import BaseCommand
from api.tests.seeds import seed_data


class Command(BaseCommand):
    help = 'Seeds the database with initial data'

    def handle(self, *args, **options):
        seed_data()
