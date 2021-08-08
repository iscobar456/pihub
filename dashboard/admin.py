from django.contrib import admin
from dashboard.models import Device, Profile, SocialConnection

# Register your models here.

class DeviceAdmin(admin.ModelAdmin):
    pass


# Registrations
admin.site.register(Device, DeviceAdmin)
admin.site.register(Profile)
admin.site.register(SocialConnection)