from django_filters import rest_framework as filters
from rest_framework import generics
from api.filters import BookingFilter
from api.models import Booking
from api.serializers.bookings import BookingWriteSerializer, BookingReadSerializer
from api.views.mixins import CustomBookingDestroyMixin, CustomSerializerByMethodMixin, CustomBookingListMixin, \
    CustomBookingCreateMixin


class BookingView(CustomSerializerByMethodMixin,
                  CustomBookingListMixin,
                  CustomBookingDestroyMixin,
                  CustomBookingCreateMixin,
                  generics.GenericAPIView):
    queryset = Booking.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)

    filterset_class = BookingFilter

    serializer_map = {
        'GET': BookingReadSerializer,
        'POST': BookingWriteSerializer
    }

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request):
        return self.destroy(request)
