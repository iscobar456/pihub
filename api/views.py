from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from dashboard.models import Device
from api.decorators import protected_endpoint
import secrets
import hashlib
import traceback

# Create your views here.

def identify_device(request):
    print("request hits - identify")
    print("Data is", request.POST)
    get_object_or_404(Device, public_key=request.POST.get('pubkey'))
    return HttpResponse("Valid public key")

def verify_device(request):
    print("request hits - verify")
    print("Data is", request.POST)
    device = get_object_or_404(Device, public_key=request.POST.get('pubkey'))
    print(device.name)

    request_hash = hashlib.sha256()
    request_hash.update(request.POST.get('pubkey'))
    request_hash.update(request.POST.get('time'))
    request_hash.update(device.secret_key)
    hash_string = request_hash.hexdigest()

    if not hash_string == request.POST.get('verification'):
        return HttpResponse('Request could not be verified, make sure your information is correct.', status=401)
    else:
        device.is_live = True
        device.save()
        return HttpResponse("Verified")

@protected_endpoint
def device_update(request):
    req_data = request.POST.copy()

    device = get_object_or_404(Device, public_key=req_data["pubkey"])
    device.ip_address = request.META.get('REMOTE_ADDR')
    device.hostname = request.META.get('REMOTE_HOST')
    device.is_live = True
    device.save()

    return HttpResponse(status=200)