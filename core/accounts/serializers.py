from django.contrib.auth import authenticate

from rest_framework import serializers

from phonenumber_field.modelfields import PhoneNumberField


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
                raise serializers.ValidationError("Неверный телефон или пароль")
        else:
            raise serializers.ValidationError("Введите телефон и пароль")

        attrs['user'] = user
        return attrs

