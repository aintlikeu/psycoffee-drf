from collections import defaultdict

import redis
from django.core.cache import cache
from rest_framework import status
from rest_framework.response import Response
from rest_framework.settings import api_settings

redis_instance = redis.StrictRedis(host='127.0.0.1', port=6379, db=1)

class CustomSerializerByMethodMixin:
    """
    Mixin to allow different serializers to be used depending on the request method type.
    """
    def get_serializer_class(self, *args, **kwargs):
        return self.serializer_map.get(self.request.method, self.serializer_class)


class CustomCreateMixin:
    """
    Mixin to create Spots, Bookings, Patients
    """
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"success": True}, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}


class CustomSpotListMixin:
    """
    Mixin for listing Spot instances, grouped by date.
    Used in spots and free_spots endpoints
    """
    def list(self, request, *args, **kwargs):
        customer_id = self.request.query_params.get('customer_id')
        date = self.request.query_params.get('date')

        # if customer_id is None or date is None:
        #     return Response(status=status.HTTP_400_BAD_REQUEST)

        # Check if the data is already cached
        cache_key = f'{request.get_full_path()}'
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            return Response(cached_data)

        queryset = self.filter_queryset(self.get_queryset())

        # group spots by date
        grouped_data = defaultdict(list)
        for spot in queryset:
            data = self.get_serializer(spot).data
            date = list(data.keys())[0]
            spot_info = list(data.values())[0]
            grouped_data[date].append(spot_info)

        # Cache the data
        response_data = {'spots': dict(grouped_data)}
        cache.set(cache_key, response_data, timeout=60*60)

        return Response(response_data)
