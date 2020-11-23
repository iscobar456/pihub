from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Device(models.Model):
    name = models.CharField(blank=True, unique=True, max_length=512)
    description = models.CharField(blank=True, max_length=512)
    owner = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    ip_address = models.CharField(blank=True, max_length=64)
    is_live = models.BooleanField(null=True)
    public_key = models.CharField(blank=True, max_length=32)
    private_key = models.CharField(blank=True, max_length=64)
    hostname = models.CharField(blank=True, max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)