from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager

from phonenumber_field.modelfields import PhoneNumberField


class UserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError('The phone must be set')
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(phone, password, **extra_fields)


class User(AbstractUser):
    # username = None
    username = models.TextField(blank=True, default="", max_length=500)
    phone = PhoneNumberField(unique=False, region="RU")
    description = models.TextField(blank=True, default="", max_length=500)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.phone}'

    class Meta:
        ordering = ('id',)


class Customer(User):
    class Meta:
        verbose_name = 'Customer'


class Patient(User):
    class Meta:
        verbose_name = 'Patient'
