from collections import defaultdict

from django_filters import rest_framework as filters
from rest_framework import generics, status
from rest_framework.response import Response

from api.filters import BookingFilter
from api.messages import NO_FIELDS_CUSTOMER_DATE_TIME
from api.models import Booking
from api.serializers.bookings import BookingWriteSerializer, BookingReadSerializer
from api.services.bookings_crud import delete_bookings
from api.views.mixins import CustomSerializerByMethodMixin, CustomCreateMixin


class BookingView(CustomSerializerByMethodMixin,
                  CustomCreateMixin,
                  generics.GenericAPIView):
    queryset = Booking.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)

    filterset_class = BookingFilter

    serializer_map = {
        'GET': BookingReadSerializer,
        'POST': BookingWriteSerializer
    }

    def get(self, request, *args, **kwargs):
        customer_id = self.request.query_params.get('customer_id')
        date = self.request.query_params.get('date')

        # if customer_id is None or date is None:
        #     return Response(status=status.HTTP_400_BAD_REQUEST)

        queryset = self.filter_queryset(self.get_queryset())

        grouped_data = defaultdict(list)

        # group bookings by date
        for booking in queryset:
            data = self.get_serializer(booking).data
            date = list(data.keys())[0]
            booking_info = list(data.values())[0]
            grouped_data[date].append(booking_info)

        return Response({'bookings': dict(grouped_data)})

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request):
        customer_id = self.request.data.get('customer_id')
        date = self.request.data.get('date')
        time = self.request.data.get('time')

        if customer_id is None or date is None or time is None:
            return Response({'success': False,
                             'errors': {'general': NO_FIELDS_CUSTOMER_DATE_TIME}},
                            status=status.HTTP_404_NOT_FOUND)

        try:
            delete_bookings(customer_id, date, time)
            return Response({'success': True}, status=status.HTTP_200_OK)
        except (TypeError, ValueError) as e:
            return Response({'success': False,
                             'errors': {'general': str(e)}},
                            status=status.HTTP_400_BAD_REQUEST)
