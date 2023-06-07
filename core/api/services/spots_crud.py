from datetime import datetime
from django.db import models
from api.models import Spot, Customer
from api.services.date_handlers import unix_to_date


def delete_spots(customer_id: int,
                 unix_timestamp: int,
                 time_str: str | None = None) -> None:
    date = unix_to_date(unix_timestamp)
    queryset = Spot.objects.filter(customer__id=customer_id, date=date)

    if time_str:
        time = datetime.strptime(time_str, "%H:%M").time()
        queryset = queryset.filter(time=time)

    queryset.delete()


def overwrite_spot(customer: Customer,
                   date: models.DateField,
                   time: models.TimeField,
                   duration: models.IntegerField) -> Spot | None:
    spot = Spot.objects.filter(customer=customer, date=date, time=time).first()

    if spot:
        spot.duration = duration
        spot.save()
        return spot

    return None


def get_spot(customer_id: int,
             unix_timestamp: int,
             time_str: str,
             duration: int) -> Spot | None:
    date = unix_to_date(unix_timestamp)
    time = datetime.strptime(time_str, "%H:%M").time()
    return Spot.objects.filter(customer__id=customer_id, date=date, time=time, duration=duration).first()
