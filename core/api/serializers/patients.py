from rest_framework import serializers

from accounts.models import Patient


class PatientSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Patient
        fields = ('id', 'email', 'password')
