from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Device(models.Model):
    name = models.CharField(blank=True, unique=True, max_length=512)
    description = models.CharField(blank=True, max_length=512)
    owner = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    ip = models.CharField(blank=True, max_length=64)
    device_id = models.CharField(blank=True, max_length=32)
    hostname = models.CharField(blank=True, max_length=64)
    