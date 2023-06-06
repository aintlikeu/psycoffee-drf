from rest_framework import serializers
from datetime import datetime

from api.models import Spot


class SpotSerializer(serializers.ModelSerializer):
    # spot = serializers.IntegerField(write_only=True)

    class Meta:
        model = Spot
        fields = '__all__'

    def to_internal_value(self, data):
        unix_timestamp = data.get('date')

        if unix_timestamp:
            try:
                date = datetime.fromtimestamp(unix_timestamp)
            except ValueError as e:
                raise serializers.ValidationError({'date': 'Некорректный формат даты.'})

        ...
