from datetime import datetime
from django.db import models


# Create your models here.
class Location(models.Model):
    name = models.CharField(max_length=100, null=True)
    province = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100, null=True)
    started_date = models.DateTimeField(default=datetime.now)


class Device(models.Model):
    name = models.CharField(max_length=100, null=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)


class Data(models.Model):
    tr = models.CharField(max_length=20, null=True)
    tm = models.CharField(max_length=20, null=True)
    ph = models.CharField(max_length=20, null=True)
    hu = models.CharField(max_length=20, null=True)
    wt = models.CharField(max_length=20, null=True)
    time = models.DateTimeField(null=True)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)


class Subscriber(models.Model):
    phone_number = models.CharField(max_length=500, null=True)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
