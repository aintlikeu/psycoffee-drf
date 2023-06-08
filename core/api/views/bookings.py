from django_filters import rest_framework as filters
from rest_framework import generics

from api.filters.spots import BookingFilter
from api.models import Booking
from api.serializers.bookings import BookingWriteSerializer, BookingReadSerializer


class BookingView(generics.ListAPIView,
                     generics.CreateAPIView,
                     generics.DestroyAPIView):

    queryset = Booking.objects.all()
    serializer_class = BookingWriteSerializer
    filter_backends = (filters.DjangoFilterBackend,)

    filterset_class = BookingFilter

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return BookingWriteSerializer
        else:
            return BookingReadSerializer
