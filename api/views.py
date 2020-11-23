from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from dashboard.models import Device
from api.decorators import device_call
import secrets
import hashlib
import traceback

# Create your views here.

@device_call
def device_update(request):
    req_data = request.POST.copy()

    device = get_object_or_404(Device, public_key=req_data["pubkey"])
    device.ip_address = request.META.get('REMOTE_ADDR')
    device.hostname = request.META.get('REMOTE_HOST')
    device.is_live = True
    device.save()

    return HttpResponse(status=200)