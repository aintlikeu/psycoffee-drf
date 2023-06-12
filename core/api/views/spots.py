from collections import defaultdict

from rest_framework import status, generics, mixins

from django_filters import rest_framework as filters
from rest_framework.response import Response

from api.exceptions import DateConversionError, TimeConversionError
from api.filters import SpotFilter
from api.models import Spot
from api.serializers.spots import SpotWriteSerializer, SpotReadSerializer
from api.services.spots_crud import delete_spots


class SimpleSpotView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Spot.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = SpotFilter

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return SpotWriteSerializer
        return SpotReadSerializer

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        grouped_data = defaultdict(list)
        for spot in queryset:
            data = self.get_serializer(spot).data
            date = list(data.keys())[0]
            time_duration = list(data.values())[0]
            grouped_data[date].append(time_duration)

        return Response({'spots': dict(grouped_data)})

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request):
        customer_id = self.request.data.get('customer_id')
        date = self.request.data.get('date')
        time = self.request.data.get('time')

        if customer_id and date:
            try:
                delete_spots(customer_id, date, time)
                return Response(status=status.HTTP_204_NO_CONTENT)
            except (DateConversionError, TimeConversionError) as e:
                return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_404_NOT_FOUND)


class FreeSpotView(generics.ListAPIView):
    queryset = Spot.objects.filter(booking=None)
    serializer_class = SpotReadSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = SpotFilter
