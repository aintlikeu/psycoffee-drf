from django.contrib.auth import authenticate

from rest_framework import serializers

from api.messages import INCORRECT_PHONE_OR_PASSWORD, REQUIRED_PHONE_AND_PASSWORD


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

    def validate(self, attrs):
        phone = attrs.get('phone')
        password = attrs.get('password')

        if phone and password:
            # Try to authenticate the user using Django auth framework
            user = authenticate(request=self.context.get('request'),
                                phone=phone,
                                password=password)
            if not user:
                # If there is no user with this credentials
                raise serializers.ValidationError({'general': INCORRECT_PHONE_OR_PASSWORD})
        else:
            raise serializers.ValidationError({'general': REQUIRED_PHONE_AND_PASSWORD})

        attrs['user'] = user
        return attrs

