from django.db import models
from accounts.models import Customer, Patient


class Spot(models.Model):
    date = models.DateField()
    time = models.TimeField()
    duration = models.IntegerField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)


class Booking(models.Model):
    spot = models.ForeignKey(Spot, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
