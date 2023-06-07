import datetime
from calendar import Calendar


def get_date_range(input_date: datetime.date) -> tuple[datetime.date, ...]:
    calendar = Calendar(firstweekday=0)
    calendar_month = calendar.monthdatescalendar(input_date.year, input_date.month)
    start_date = calendar_month[0][0]
    end_date = calendar_month[-1][-1]
    return start_date, end_date


def unix_to_date(unix_timestamp: int | str) -> datetime.date:
    return datetime.datetime.fromtimestamp(int(unix_timestamp)).date()
