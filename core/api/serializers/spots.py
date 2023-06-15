from rest_framework import serializers
from datetime import datetime

from accounts.models import Customer
from api.models import Spot
from api.services import date_handlers, spots_crud
from api.messages import INCORRECT_DATE_FORMAT, INCORRECT_SPOT_TIME, CUSTOMER_DOES_NOT_EXIST, SPOT_ALREADY_EXIST, \
    INCORRECT_DATE, INCORRECT_SPOT_DURATION

DURATION_VALUES = (60, 90, 120)


class CustomDateField(serializers.IntegerField):
    # Custom field for returning custom error message
    default_error_messages = {
        "invalid": INCORRECT_DATE_FORMAT
    }


class CustomTimeField(serializers.TimeField):
    # Custom field for returning custom error message
    default_error_messages = {
        "invalid": INCORRECT_SPOT_TIME
    }


class SpotWriteSerializer(serializers.ModelSerializer):
    date = CustomDateField(write_only=True)
    time = CustomTimeField(write_only=True, format="%H:%M")
    customer_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Spot
        fields = ['id', 'date', 'time', 'duration', 'customer_id']

    def create(self, validated_data):
        customer = validated_data.get('customer')
        date = validated_data.get('date')
        time = validated_data.get('time')
        duration = validated_data.get('duration')

        # if the spot with the same (customer, date, time) exists,
        # overwrite duration without creating new object
        spot_existed = spots_crud.overwrite_spot(customer, date, time, duration)
        if spot_existed:
            return spot_existed

        return super().create(validated_data)

    def validate(self, data):
        # if customer exists, replace 'customer_id' field by 'customer', else raise error
        customer_id = data.pop('customer_id')
        try:
            data['customer'] = Customer.objects.get(pk=customer_id)
        except Customer.DoesNotExist:
            raise serializers.ValidationError({'general': CUSTOMER_DOES_NOT_EXIST})

        # if spot exists, raise error
        spot_exist = Spot.objects.filter(date=data['date'],
                                         time=data['time'],
                                         customer=data['customer'],
                                         duration=data['duration']).exists()
        if spot_exist:
            raise serializers.ValidationError({'general': SPOT_ALREADY_EXIST})

        return data

    def validate_date(self, unix_timestamp):
        # check that date is valid
        try:
            date = date_handlers.unix_to_date(unix_timestamp)
        except (TypeError, ValueError):
            raise serializers.ValidationError(INCORRECT_DATE_FORMAT)
        # check that date is in the future
        if date < datetime.now().date():
            raise serializers.ValidationError(INCORRECT_DATE)

        return date

    def validate_duration(self, duration):
        # check that duration is in the predefined list
        if duration not in DURATION_VALUES:
            raise serializers.ValidationError(INCORRECT_SPOT_DURATION)
        return duration


class SpotReadSerializer(serializers.ModelSerializer):
    date = serializers.DateField(format="%d.%m.%Y")
    time = serializers.TimeField(format="%H:%M")

    class Meta:
        model = Spot
        fields = ['id', 'date', 'time', 'duration', 'customer_id']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return {representation['date']: {
            "id": representation['id'],
            "time": representation['time'],
            "duration": representation['duration'],
            "customer_id": representation['customer_id']}
        }


class FreeSpotReadSerializer(SpotReadSerializer):
    duration = serializers.SerializerMethodField()

    def get_duration(self, obj):
        return [i for i in DURATION_VALUES if i <= obj.duration]
