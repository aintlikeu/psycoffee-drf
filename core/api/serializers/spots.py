from rest_framework import serializers
from datetime import datetime

from api.models import Spot
from api.services import date_handlers, spots_crud

DURATION_VALUES = (60, 90, 120)


class SpotWriteSerializer(serializers.ModelSerializer):
    date = serializers.IntegerField(write_only=True)

    class Meta:
        model = Spot
        fields = '__all__'

    def create(self, validated_data):
        customer = validated_data.get('customer')
        date = validated_data.get('date')
        time = validated_data.get('time')
        duration = validated_data.get('duration')

        # if the spot already exists, rewrite duration without creating new instance
        spot_existed = spots_crud.overwrite_spot(customer, date, time, duration)
        if spot_existed:
            return spot_existed

        return super().create(validated_data)

    def validate_date(self, unix_timestamp):
        try:
            date = date_handlers.unix_to_date(unix_timestamp)
        except ValueError:
            raise serializers.ValidationError('Некорректный формат даты.')

        if date < datetime.now().date():
            raise serializers.ValidationError('Дата окна не может быть в прошлом.')

        return date

    def validate_duration(self, duration):
        if duration not in DURATION_VALUES:
            raise serializers.ValidationError(f'Возможные интервалы сессии - {DURATION_VALUES} минут.')
        return duration


class SpotReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spot
        fields = ['customer', 'date', 'time', 'duration', 'booking']
