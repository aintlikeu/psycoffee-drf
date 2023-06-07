from rest_framework import serializers
from datetime import datetime

from api.models import Spot
from api.services import date_handlers

DURATION_VALUES = (60, 90, 120)


class SpotWriteSerializer(serializers.ModelSerializer):
    date = serializers.IntegerField(write_only=True)

    class Meta:
        model = Spot
        fields = '__all__'

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
        fields = '__all__'
