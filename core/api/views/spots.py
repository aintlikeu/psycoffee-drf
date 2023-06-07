from rest_framework import status, generics

from django_filters import rest_framework as filters
from rest_framework.response import Response

from api.filters.spots import SpotFilter
from api.models import Spot
from api.serializers.spots import SpotWriteSerializer, SpotReadSerializer
from api.services.spots_crud import delete_spots


class SimpleSpotView(generics.ListAPIView,
                     generics.CreateAPIView):
    queryset = Spot.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)

    filterset_class = SpotFilter

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return SpotWriteSerializer
        return SpotReadSerializer

    def delete(self, request):
        customer_id = self.request.data.get('customer_id')
        date = self.request.data.get('date')
        time = self.request.data.get('time')

        if customer_id and date:
            delete_spots(customer_id, date, time)
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_404_NOT_FOUND)
