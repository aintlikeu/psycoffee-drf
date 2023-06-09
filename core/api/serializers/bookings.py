from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from api.models import Booking, Spot
from api.serializers.spots import SpotReadSerializer


class BookingWriteSerializer(serializers.ModelSerializer):
    spot_id = serializers.IntegerField(write_only=True)
    duration = serializers.IntegerField(write_only=True)

    class Meta:
        model = Booking
        fields = ['spot_id', 'duration', 'name', 'phone', 'comment']

    def create(self, validated_data):
        spot_id = validated_data.pop('spot_id')
        duration = validated_data.pop('duration')

        spot = get_object_or_404(Spot, pk=spot_id)

        if not hasattr(spot, 'booking'):
            if spot.duration == duration:
                validated_data['spot'] = spot
                return super().create(validated_data)
            else:
                raise serializers.ValidationError('The spot duration is wrong')
        else:
            raise serializers.ValidationError('The spot is already booked')


class BookingReadSerializer(serializers.ModelSerializer):
    spot = SpotReadSerializer()

    class Meta:
        model = Booking
        fields = '__all__'
