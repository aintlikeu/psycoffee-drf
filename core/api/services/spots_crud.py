from datetime import datetime

from api.models import Spot
from api.services.date_handlers import unix_to_date


def delete_spots(customer_id: int, unix_timestamp: int, time_str: str | None = None):
    date = unix_to_date(unix_timestamp)
    queryset = Spot.objects.filter(customer__id=customer_id, date=date)
    if time_str:
        time = datetime.strptime(time_str, "%H:%M").time()
        queryset = queryset.filter(time=time)
    queryset.delete()
