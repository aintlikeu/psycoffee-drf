from django_filters import rest_framework as filters

from api.models import Spot
from api.services import date_handlers


class SpotFilter(filters.FilterSet):
    customer_id = filters.NumberFilter(field_name='customer__id')
    date = filters.NumberFilter(field_name='date', method='filter_date')

    class Meta:
        model = Spot
        fields = ['customer', 'date']

    def filter_date(self, queryset, name, value):
        """
        Filter spots by date.
        If whole_month is set to true, return spots for the entire month,
        including any days from other months that are part of incomplete weeks.
        """
        try:
            date = date_handlers.unix_to_date(value)
        except ValueError:
            return queryset

        whole_month = self.request.query_params.get('whole_month', '').lower() == 'true'
        if whole_month:
            date_range = date_handlers.get_date_range(date)
            return queryset.filter(date__range=date_range)

        return queryset.filter(date=date)
