from django_filters import rest_framework as filters

from api.models import Spot, Booking
from api.services import date_handlers


class BaseFilter(filters.FilterSet):
    def filter_date(self, queryset, name, value):
        """
        Filter spots/bookings by date.
        If whole_month is set to true, return spots for the entire month,
        including any days from other months that are part of incomplete weeks.
        """
        try:
            date = date_handlers.unix_to_date(value)
        except ValueError:
            return queryset

        # we need to differentiate "date" field for different models,
        # because we don't have this field in Booking model,
        # we must access it through "spot" field
        date_field = 'date'
        if self.Meta.model == Booking:
            date_field = 'spot__date'

        whole_month = self.request.query_params.get('whole_month', '').lower() == 'true'
        if whole_month:
            date_range = date_handlers.get_date_range(date)
            return queryset.filter(**{f'{date_field}__range': date_range})

        return queryset.filter(**{date_field: date})


class SpotFilter(BaseFilter):
    customer_id = filters.NumberFilter(field_name='customer__id')
    date = filters.NumberFilter(field_name='date', method='filter_date')

    class Meta:
        model = Spot
        fields = ['customer', 'date']


class BookingFilter(BaseFilter):
    customer_id = filters.NumberFilter(field_name='spot__customer__id')
    date = filters.NumberFilter(field_name='spot__date', method='filter_date')

    class Meta:
        model = Booking
        fields = ['spot__customer__id', 'spot__date']
