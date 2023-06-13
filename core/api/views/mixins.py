from collections import defaultdict

from rest_framework import status
from rest_framework.response import Response
from rest_framework.settings import api_settings

from api.exceptions import DateConversionError, TimeConversionError
from api.services.bookings_crud import delete_bookings
from api.services.spots_crud import delete_spots


class CustomSerializerByMethodMixin:
    def get_serializer_class(self, *args, **kwargs):
        return self.serializer_map.get(self.request.method, self.serializer_class)


class CustomSpotListMixin:
    def list(self, request, *args, **kwargs):
        customer_id = self.request.query_params.get('customer_id')
        date = self.request.query_params.get('date')

        # if customer_id is None or date is None:
        #     return Response(status=status.HTTP_400_BAD_REQUEST)

        queryset = self.filter_queryset(self.get_queryset())

        grouped_data = defaultdict(list)
        for spot in queryset:
            data = self.get_serializer(spot).data
            date = list(data.keys())[0]
            time_duration = list(data.values())[0]
            grouped_data[date].append(time_duration)

        return Response({'spots': dict(grouped_data)})


class CustomSpotDestroyMixin:
    def destroy(self, request):
        customer_id = self.request.data.get('customer_id')
        date = self.request.data.get('date')
        time = self.request.data.get('time')

        if customer_id is None or date is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            delete_spots(customer_id, date, time)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except (DateConversionError, TimeConversionError) as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CustomSpotCreateMixin:
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


class CustomBookingListMixin:
    def list(self, request, *args, **kwargs):
        customer_id = self.request.query_params.get('customer_id')
        date = self.request.query_params.get('date')

        # if customer_id is None or date is None:
        #     return Response(status=status.HTTP_400_BAD_REQUEST)

        queryset = self.filter_queryset(self.get_queryset())

        grouped_data = defaultdict(list)
        for booking in queryset:
            data = self.get_serializer(booking).data
            date = list(data.keys())[0]
            time_duration = list(data.values())[0]
            grouped_data[date].append(time_duration)

        return Response({'bookings': dict(grouped_data)})


class CustomBookingDestroyMixin:
    def destroy(self, request):
        customer_id = self.request.data.get('customer_id')
        date = self.request.data.get('date')
        time = self.request.data.get('time')

        if customer_id is None or date is None or time is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            delete_bookings(customer_id, date, time)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except (DateConversionError, TimeConversionError) as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CustomBookingCreateMixin:
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