from rest_framework import generics, mixins

from django_filters import rest_framework as filters
from api.filters import SpotFilter
from api.models import Spot
from api.serializers.spots import SpotWriteSerializer, SpotReadSerializer
from api.views.mixins import CustomSerializerByMethodMixin, CustomSpotListMixin, CustomSpotDestroyMixin


class SimpleSpotView(CustomSerializerByMethodMixin,
                     CustomSpotListMixin,
                     CustomSpotDestroyMixin,
                     mixins.CreateModelMixin,
                     generics.GenericAPIView):
    queryset = Spot.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = SpotFilter

    serializer_map = {
        'GET': SpotReadSerializer,
        'POST': SpotWriteSerializer
    }

    def get(self, request, *args, **kwargs):
        return self.list(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request):
        return self.destroy(request)


class FreeSpotView(generics.ListAPIView):
    queryset = Spot.objects.filter(booking=None)
    serializer_class = SpotReadSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = SpotFilter
