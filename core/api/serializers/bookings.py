from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from api.models import Booking, Spot


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


class BookingInfoSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    time = serializers.TimeField(source='spot.time')
    duration = serializers.IntegerField(source='spot.duration')

    class Meta:
        model = Booking
        fields = ['id', 'time', 'duration']


class BookingReadSerializer(serializers.Serializer):
    date = serializers.DateField(source='spot.date', format="%d.%m.%Y")
    booking_info = BookingInfoSerializer(source='*', read_only=True)

    class Meta:
        model = Booking
        fields = ['date', 'booking_info']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return {representation['date']: representation['booking_info']}
