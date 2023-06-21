from rest_framework import generics, status
from django_filters import rest_framework as filters
from rest_framework.response import Response

from api.filters import SpotFilter
from api.messages import NO_FIELDS_CUSTOMER_DATE
from api.models import Spot
from api.serializers.spots import SpotWriteSerializer, SpotReadSerializer, FreeSpotReadSerializer
from api.services.spots_crud import delete_spots
from api.views.mixins import CustomSerializerByMethodMixin, CustomCreateMixin, CustomSpotListMixin


class SimpleSpotView(CustomSerializerByMethodMixin,
                     CustomSpotListMixin,
                     CustomCreateMixin,
                     generics.GenericAPIView):
    queryset = Spot.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = SpotFilter

    serializer_map = {
        'GET': SpotReadSerializer,
        'POST': SpotWriteSerializer
    }

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request):
        customer_id = self.request.data.get('customer_id')
        date = self.request.data.get('date')
        time = self.request.data.get('time')

        if customer_id is None or date is None:
            return Response({'success': False,
                             'errors': {'general': NO_FIELDS_CUSTOMER_DATE}},
                            status=status.HTTP_404_NOT_FOUND)

        try:
            delete_spots(customer_id, date, time)
            return Response({'success': True}, status=status.HTTP_200_OK)
        except (TypeError, ValueError) as e:
            return Response({'success': False,
                             'errors': {'general': str(e)}},
                            status=status.HTTP_400_BAD_REQUEST)


class FreeSpotView(CustomSpotListMixin,
                   generics.GenericAPIView):
    queryset = Spot.objects.filter(booking=None)
    serializer_class = FreeSpotReadSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = SpotFilter

    def get(self, request, *args, **kwargs):
        return self.list(self, request, *args, **kwargs)
