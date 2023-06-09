from django.core.management.base import BaseCommand

from datetime import date, time, timedelta

from yaml import safe_load

from accounts.models import Customer
from api.tests.factories import CustomerFactory, SpotFactory, BookingFactory


# seeding settings
with open('./config.yaml', 'r') as f:
    config = safe_load(f)

seeding_config = config['seeding']

CUSTOMER_QTY = seeding_config['customer_qty']
DATE_QTY = seeding_config['date_qty']
TIME_START = seeding_config['time_start']
TIME_END = seeding_config['time_end']
TIME_STEP = seeding_config['time_step']
BOOKING_SHARE = seeding_config['booking_share']


def seed_data():
    # clear the database. All other tables have foreign keys, so they also will be cleared
    Customer.objects.all().delete()

    # list of dates from tomorrow to X days forward
    date_list = [date.today() + timedelta(days=x + 1) for x in range(DATE_QTY)]
    # list of time
    time_list = [time(hour) for hour in range(TIME_START, TIME_END, TIME_STEP)]

    customer_instances = CustomerFactory.create_batch(CUSTOMER_QTY)

    spot_instances = [
        SpotFactory.create(customer=customer, date=date_, time=time_)
        for customer in customer_instances
        for date_ in date_list
        for time_ in time_list
    ]

    booking_instances = BookingFactory.create_batch(int(len(spot_instances) * BOOKING_SHARE))

    print(f'Seeded:\n\tCustomers: {CUSTOMER_QTY}\n\tSpots: {len(spot_instances)}\n\tBookings: {len(booking_instances)}')


class Command(BaseCommand):
    help = 'Seeds the database with initial data'

    def handle(self, *args, **options):
        seed_data()
