import random
import datetime

import factory

from accounts.models import Customer
from api.models import Spot, Booking

from api.serializers.spots import DURATION_VALUES


class CustomerFactory(factory.django.DjangoModelFactory):
    phone = factory.Sequence(lambda n: '+79%08d' % n)
    password = factory.PostGenerationMethodCall('set_password', 'password123')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')

    class Meta:
        model = Customer


# Prefer to use with the argument customer=(Customer object)
# customer defined as factory.Iterator to prevent creating new instances of Customer
class SpotFactory(factory.django.DjangoModelFactory):
    date = factory.Faker('future_date', end_date='+30d')
    # time = factory.Faker('time_object')
    time = factory.LazyAttribute(lambda o: datetime.time(hour=random.randint(0, 23), minute=random.randint(0, 59)))
    duration = factory.Faker('random_element', elements=DURATION_VALUES)
    customer = factory.Iterator(Customer.objects.all())

    class Meta:
        model = Spot


# Prefer to use with the argument spot=(Spot object)
# spot defined as factory.Iterator to prevent creating new instances of Spot
class BookingFactory(factory.django.DjangoModelFactory):
    # order_by('?') shuffles queryset
    spot = factory.Iterator(Spot.objects.filter(booking=None).order_by('?'))
    name = factory.Faker('name')
    # use here the format of the phone, which is slightly different from the customer's phone format
    # just to differentiate
    phone = factory.Sequence(lambda n: '+799%07d' % n)
    comment = factory.Faker('sentence')
    duration = factory.LazyAttribute(lambda o: random.choice([i for i in DURATION_VALUES if i <= o.spot.duration]))

    class Meta:
        model = Booking
