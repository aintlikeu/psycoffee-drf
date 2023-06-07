from rest_framework.generics import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response

from api.models import Spot
from api.serializers.spots import SpotWriteSerializer, SpotReadSerializer
from api.services import date_services


class SimpleSpotViewSet(viewsets.ViewSet):
    def get_queryset(self):
        queryset = Spot.objects.all()
        customer_id = self.request.query_params.get('customer_id')
        unix_timestamp = self.request.query_params.get('date')

        whole_month = self.request.query_params.get('whole_month')

        if customer_id:
            queryset = queryset.filter(customer=customer_id)

        if unix_timestamp:
            date = date_services.unix_to_date(unix_timestamp)

            if whole_month.lower() == 'true':
                queryset = queryset.filter(date__range=(date_services.get_date_range(date)))
            else:
                queryset = queryset.filter(date=date)

        return queryset

    def list(self, request):
        serializer = SpotReadSerializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = SpotWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        spot = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = SpotReadSerializer(spot, many=False)
        return Response(serializer.data)

    # def destroy(self, request, pk=None):
    #     spot = get_object_or_404(self.queryset, pk=pk)
    #     spot.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)
