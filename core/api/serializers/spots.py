from rest_framework import serializers
from datetime import datetime

from api.models import Spot

DURATION_VALUES = (60, 90, 120)


class SpotSerializer(serializers.ModelSerializer):
    date = serializers.IntegerField(write_only=True)

    class Meta:
        model = Spot
        fields = '__all__'

    def validate_date(self, unix_timestamp):
        try:
            date = datetime.fromtimestamp(int(unix_timestamp)).date()
        except ValueError:
            raise serializers.ValidationError('Некорректный формат даты.')

        if date < datetime.now().date():
            raise serializers.ValidationError('Дата окна не может быть в прошлом.')

        return date

    def validate_duration(self, duration):
        if duration not in DURATION_VALUES:
            raise serializers.ValidationError(f'Возможные интервалы сессии - {DURATION_VALUES} минут.')
        return duration


        # https://www.django-rest-framework.org/api-guide/serializers/

        # {"date": 1686104718, "time": "11:00", "duration": 60, "customer": 2}

        # {"date": 1686018318, "time": "11:00", "duration": 60, "customer": 2}
