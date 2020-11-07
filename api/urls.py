from django.urls import path
from . import views

urlpatterns = [
    path('update_ip', views.update_ip)
]