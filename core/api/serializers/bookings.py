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


class BookingReadSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    date = serializers.DateField(source='spot.date', format="%d.%m.%Y")
    time = serializers.TimeField(source='spot.time')
    customer_id = serializers.IntegerField(source='spot.customer_id')
    duration = serializers.IntegerField(source='spot.duration')

    class Meta:
        model = Booking
        fields = ['id', 'date', 'time', 'customer_id', 'duration']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return {representation['date']: {
            "id": representation['id'],
            "time": representation['time'],
            "duration": representation['duration'],
            "customer_id": representation['customer_id']}
        }
