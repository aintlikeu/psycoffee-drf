from rest_framework.generics import ListCreateAPIView, DestroyAPIView, get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response

from api.models import Spot
from api.serializers.spots import SpotSerializer


class SimpleSpotViewSet(viewsets.ViewSet):
    queryset = Spot.objects.all()
    serializer_class = SpotSerializer

    def list(self, request):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        spot = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(spot, many=False)
        return Response(serializer.data)

    # def destroy(self, request, pk=None):
    #     spot = get_object_or_404(self.queryset, pk=pk)
    #     spot.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)
