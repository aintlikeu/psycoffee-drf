import datetime
from calendar import Calendar

from api.exceptions import DateConversionError, TimeConversionError


def get_date_range(input_date: datetime.date) -> tuple[datetime.date, ...]:
    calendar = Calendar(firstweekday=0)
    calendar_month = calendar.monthdatescalendar(input_date.year, input_date.month)
    start_date = calendar_month[0][0]
    end_date = calendar_month[-1][-1]
    return start_date, end_date


def unix_to_date(unix_timestamp: int | str) -> datetime.date:
    try:
        return datetime.datetime.fromtimestamp(int(unix_timestamp)).date()
    except (ValueError, TypeError):
        raise DateConversionError(f'Could not convert unix_timestamp: {unix_timestamp}')


def time_from_string(time_str: str) -> datetime.time:
    try:
        return datetime.datetime.strptime(time_str, "%H:%M").time()
    except ValueError:
        raise TimeConversionError(f'Could not convert time_str: {time_str}')
