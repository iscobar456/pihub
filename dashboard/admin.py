from django.contrib import admin
from dashboard.models import Device

# Register your models here.

class DeviceAdmin(admin.ModelAdmin):
    pass


# Registrations
admin.site.register(Device, DeviceAdmin)