from django.urls import path
from . import views

urlpatterns = [
    path('identify-device', views.identify_device),
    path('device-update', views.device_update),
    path('verify-device', views.device_update),
]