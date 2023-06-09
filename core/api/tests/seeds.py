from datetime import date, time, timedelta

from accounts.models import Customer
from api.tests.factories import CustomerFactory, SpotFactory, BookingFactory

# seeding settings
CUSTOMER_QTY = 5

DATE_QTY = 5

TIME_START = 8      # from 0 to 24
TIME_END = 24       # from 0 to 24
TIME_STEP = 2       # time between spots

BOOKING_SHARE = 0.5   # from 0 to 1. share of the booked spots


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
