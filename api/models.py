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
    ph = models.CharField(max_length=20, null=True)
    us = models.CharField(max_length=20, null=True)
    hd = models.CharField(max_length=20, null=True)
    ts = models.CharField(max_length=20, null=True)
    started_date = models.DateTimeField(default=datetime.now)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)


class Subscriber(models.Model):
    phone_number = models.CharField(max_length=30, null=True)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
