from collections import defaultdict

from rest_framework import status
from rest_framework.response import Response
from rest_framework.settings import api_settings

from api.messages import NO_FIELDS_CUSTOMER_DATE, NO_FIELDS_CUSTOMER_DATE_TIME
from api.services.bookings_crud import delete_bookings
from api.services.spots_crud import delete_spots


class CustomSerializerByMethodMixin:
    """
    Mixin to allow different serializers to be used depending on the request method type.
    """
    def get_serializer_class(self, *args, **kwargs):
        return self.serializer_map.get(self.request.method, self.serializer_class)


class CustomSpotListMixin:
    """
    Mixin for listing Spot instances, grouped by date.
    """
    def list(self, request, *args, **kwargs):
        customer_id = self.request.query_params.get('customer_id')
        date = self.request.query_params.get('date')

        # if customer_id is None or date is None:
        #     return Response(status=status.HTTP_400_BAD_REQUEST)

        queryset = self.filter_queryset(self.get_queryset())

        # group spots by date
        grouped_data = defaultdict(list)
        for spot in queryset:
            data = self.get_serializer(spot).data
            date = list(data.keys())[0]
            spot_info = list(data.values())[0]
            grouped_data[date].append(spot_info)

        return Response({'spots': dict(grouped_data)})


class CustomSpotDestroyMixin:
    """
    Mixin for deleting Spot instances.
    """
    def destroy(self, request):
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


# class CustomSpotCreateMixin:
#     """
#     Mixin for creating Spot instances.
#     """
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         if not serializer.is_valid():
#             return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#         return Response({"success": True}, status=status.HTTP_201_CREATED, headers=headers)
#
#     def perform_create(self, serializer):
#         serializer.save()
#
#     def get_success_headers(self, data):
#         try:
#             return {'Location': str(data[api_settings.URL_FIELD_NAME])}
#         except (TypeError, KeyError):
#             return {}


class CustomBookingListMixin:
    """
    Mixin for listing Booking instances, grouped by date.
    """
    def list(self, request, *args, **kwargs):
        customer_id = self.request.query_params.get('customer_id')
        date = self.request.query_params.get('date')

        # if customer_id is None or date is None:
        #     return Response(status=status.HTTP_400_BAD_REQUEST)

        queryset = self.filter_queryset(self.get_queryset())

        grouped_data = defaultdict(list)

        # group bookings by date
        for booking in queryset:
            data = self.get_serializer(booking).data
            date = list(data.keys())[0]
            booking_info = list(data.values())[0]
            grouped_data[date].append(booking_info)

        return Response({'bookings': dict(grouped_data)})


class CustomBookingDestroyMixin:
    """
    Mixin for deleting Booking instances.
    """
    def destroy(self, request):
        customer_id = self.request.data.get('customer_id')
        date = self.request.data.get('date')
        time = self.request.data.get('time')

        if customer_id is None or date is None or time is None:
            return Response({'success': False,
                             'errors': {'general': NO_FIELDS_CUSTOMER_DATE_TIME}},
                            status=status.HTTP_404_NOT_FOUND)

        try:
            delete_bookings(customer_id, date, time)
            return Response({'success': True}, status=status.HTTP_200_OK)
        except (TypeError, ValueError) as e:
            return Response({'success': False,
                             'errors': {'general': str(e)}},
                            status=status.HTTP_400_BAD_REQUEST)


# class CustomBookingCreateMixin:
#     """
#     Mixin for creating Booking instances.
#     """
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         if not serializer.is_valid():
#             return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#         return Response({"success": True}, status=status.HTTP_201_CREATED, headers=headers)
#
#     def perform_create(self, serializer):
#         serializer.save()
#
#     def get_success_headers(self, data):
#         try:
#             return {'Location': str(data[api_settings.URL_FIELD_NAME])}
#         except (TypeError, KeyError):
#             return {}
#

class CustomCreateMixin:
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