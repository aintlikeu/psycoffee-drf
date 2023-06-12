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

    class Meta:
        ordering = ('customer', 'date', 'time')


class Booking(models.Model):
    spot = models.OneToOneField(Spot, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = PhoneNumberField(region="RU")
    comment = models.TextField(blank=True, default="")

    def __str__(self):
        return f'{self.name} ({self.phone}) @ {self.spot.date}, {self.spot.time}, {self.spot.customer.last_name}'

    class Meta:
        ordering = ('spot',)
