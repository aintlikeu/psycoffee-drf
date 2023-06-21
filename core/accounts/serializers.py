from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from rest_framework import serializers

from accounts.models import Patient
from api.messages import INCORRECT_PHONE_OR_PASSWORD, REQUIRED_PHONE_AND_PASSWORD, PASSWORDS_DO_NOT_MATCH


class LoginSerializer(serializers.Serializer):
    """
    This serializer defines two fields for authentication:
      * phone
      * password.
    It will try to authenticate the user with when validated.
    """
    phone = serializers.CharField(label="Phone",
                                  write_only=True)
    password = serializers.CharField(label="Password",
                                     style={'input_type': 'password'},
                                     trim_whitespace=False,
                                     write_only=True)

    def validate(self, data):
        phone = data.get('phone')
        password = data.get('password')

        if phone and password:
            # Try to authenticate the user using Django auth framework
            user = authenticate(request=self.context.get('request'),
                                phone=phone,
                                password=password)
            if not user:
                # If there is no user with this credentials
                raise serializers.ValidationError({'login': INCORRECT_PHONE_OR_PASSWORD})
        else:
            raise serializers.ValidationError({'login': REQUIRED_PHONE_AND_PASSWORD})

        data['user'] = user
        return data


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = Patient
        fields = ('phone', 'password', 'password2')

    def validate(self, data):
        password = data.get('password')
        password2 = data.get('password2')

        if password and password2 and password != password2:
            raise serializers.ValidationError({'password': PASSWORDS_DO_NOT_MATCH})

        return data

    def create(self, validated_data):
        user = Patient.objects.create_user(phone=validated_data['phone'],
                                           password=validated_data['password'])
        return user
