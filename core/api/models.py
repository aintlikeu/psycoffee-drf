from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from accounts.models import Customer


class Spot(models.Model):
    date = models.DateField()
    time = models.TimeField()
    duration = models.IntegerField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.customer}: {self.time}, {self.date} duration {self.duration}'


class Booking(models.Model):
    spot = models.ForeignKey(Spot, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = PhoneNumberField(region="RU")
    comment = models.TextField()
