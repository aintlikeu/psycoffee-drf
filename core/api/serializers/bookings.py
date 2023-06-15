from rest_framework import serializers

from api.models import Booking, Spot


class BookingWriteSerializer(serializers.ModelSerializer):
    spot_id = serializers.IntegerField(write_only=True)
    duration = serializers.IntegerField()

    class Meta:
        model = Booking
        fields = ['spot_id', 'duration', 'name', 'phone', 'comment']

    def create(self, validated_data):
        return super().create(validated_data)

    def validate(self, data):
        spot_id = data.pop('spot_id')
        duration = data.get('duration')
        # check that spot exists and replace spot_id by spot, else raise error
        try:
            spot = Spot.objects.get(pk=spot_id)
        except Spot.DoesNotExist:
            raise serializers.ValidationError({'general': 'Окно с таким spot_id не существует'})

        data['spot'] = spot
        # check that the duration is correct
        if not hasattr(spot, 'booking'):
            if duration > spot.duration:
                raise serializers.ValidationError({'general': 'Неверная продолжительность сессии'})
        else:
            # check that the spot is not already booked
            raise serializers.ValidationError({'general': 'Окно уже забронировано'})

        return data


class BookingReadSerializer(serializers.ModelSerializer):
    date = serializers.DateField(source='spot.date', format="%d.%m.%Y")
    time = serializers.TimeField(source='spot.time', format="%H:%M")
    customer_id = serializers.IntegerField(source='spot.customer_id')

    class Meta:
        model = Booking
        fields = ['id', 'date', 'time', 'customer_id', 'duration', 'name', 'phone', 'comment']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return {representation['date']: {
            "id": representation['id'],
            "time": representation['time'],
            "duration": representation['duration'],
            "customer_id": representation['customer_id'],
            "name": representation['name'],
            "phone": representation['phone'],
            "comment": representation['comment']}
        }
