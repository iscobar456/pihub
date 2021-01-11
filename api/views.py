from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from dashboard.models import Device
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import secrets
import hashlib
import traceback

# Create your views here.

@csrf_exempt
def identify_device(request):
    print("request hits - identify")
    print("Data is", request.POST)
    get_object_or_404(Device, public_key=request.POST.get('public_key'))
    return HttpResponse("Valid public key")

@csrf_exempt
def verify_device(request):
    if verify_data(request):
        device = get_object_or_404(Device, public_key=request.POST.get('public_key'))
        device.is_live = True
        device.save()
        return HttpResponse("Verified")
    else:
        return HttpResponse('Request could not be verified, make sure your information is correct.', status=401)

@csrf_exempt
@require_POST
def device_update(request):
    if not verify_data(request):
        return HttpResponse('Request could not be verified, make sure your information is correct.', status=401)
    device = get_object_or_404(Device, public_key=request.POST.get("public_key"))
    device.ip_address = request.META.get('REMOTE_ADDR')
    device.hostname = request.META.get('REMOTE_HOST')
    device.is_live = True
    device.save()

    return HttpResponse(status=200)


def verify_data(request):
    device = get_object_or_404(Device, public_key=request.POST.get('public_key'))
    request_hash = hashlib.sha256()
    request_hash.update(f"{ request.POST.get('public_key') }{ request.POST.get('time') }{ device.private_key }".encode())
    hash_string = request_hash.hexdigest()
    if hash_string == request.POST.get('vhash'):
        return True
    else:
        return False