from django_filters import rest_framework as filters
from rest_framework import generics, status, mixins
from rest_framework.response import Response

from api.exceptions import DateConversionError, TimeConversionError
from api.filters import BookingFilter
from api.models import Booking
from api.serializers.bookings import BookingWriteSerializer, BookingReadSerializer
from api.services.bookings_crud import delete_bookings


class BookingView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingWriteSerializer
    filter_backends = (filters.DjangoFilterBackend,)

    filterset_class = BookingFilter

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return BookingWriteSerializer
        else:
            return BookingReadSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request):
        customer_id = self.request.data.get('customer_id')
        date = self.request.data.get('date')
        time = self.request.data.get('time')

        if customer_id and date and time:
            try:
                delete_bookings(customer_id, date, time)
                return Response(status=status.HTTP_204_NO_CONTENT)
            except (DateConversionError, TimeConversionError) as e:
                return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_404_NOT_FOUND)
