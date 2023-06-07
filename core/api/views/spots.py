from rest_framework import viewsets, mixins, status, views

from django_filters import rest_framework as filters

from api.filters.spots import SpotFilter
from api.models import Spot
from api.serializers.spots import SpotWriteSerializer, SpotReadSerializer


class SimpleSpotViewSet(mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.DestroyModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    queryset = Spot.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)

    filterset_class = SpotFilter

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return SpotWriteSerializer
        return SpotReadSerializer
