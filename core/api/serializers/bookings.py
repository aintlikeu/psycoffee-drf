from rest_framework import serializers

from api.models import Booking
from api.serializers.spots import SpotReadSerializer
from api.services import spots_crud


class BookingWriteSerializer(serializers.ModelSerializer):
    customer_id = serializers.IntegerField(write_only=True)
    date = serializers.IntegerField(write_only=True)
    time = serializers.CharField(write_only=True)
    duration = serializers.IntegerField(write_only=True)

    class Meta:
        model = Booking
        fields = ['customer_id', 'date', 'time', 'duration', 'name', 'phone', 'comment']

    def create(self, validated_data):
        customer_id = validated_data.pop('customer_id')
        date = validated_data.pop('date')
        time = validated_data.pop('time')
        duration = validated_data.pop('duration')

        spot = spots_crud.get_spot(customer_id, date, time, duration)

        if spot:
            if not hasattr(spot, 'booking'):
                validated_data['spot'] = spot
                return super().create(validated_data)
            else:
                raise serializers.ValidationError('The spot is already booked')
        else:
            raise serializers.ValidationError(f'The specified spot does not exist')


class BookingReadSerializer(serializers.ModelSerializer):
    spot = SpotReadSerializer()

    class Meta:
        model = Booking
        fields = '__all__'
