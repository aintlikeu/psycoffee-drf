from api.models import Booking
from api.services.date_handlers import unix_to_date, time_from_string


def delete_bookings(customer_id: int,
                    unix_timestamp: int,
                    time_str: str) -> None:

    date = unix_to_date(unix_timestamp)
    time = time_from_string(time_str)

    queryset = Booking.objects.filter(spot__customer__id=customer_id,
                                      spot__date=date,
                                      spot__time=time)

    queryset.delete()
