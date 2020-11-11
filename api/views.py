from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from dashboard.forms import DeviceAPIForm
from dashboard.models import Device
from api.decorators import device_call
import secrets
import hashlib
import traceback

# Create your views here.

def verify_request(request):

    user = get_object_or_404(User, username=request.POST.get('username'))

    request_hash = hashlib.sha256()
    request_hash.update(request.POST.get('username'))
    request_hash.update(request.POST.get('time'))
    request_hash.update(user.secret_key)

    hash_string = request_hash.hexdigest()

    if hash_string == request.POST.get('verification'):
        return True
    else:
        return False


@device_call
def device_update(request):
    
    if not verify_request(request):
        return HttpResponse('Request could not be verified, make sure your information is correct.', status=401)

    try:
        device = Device.objects.get(device_id=request.POST.get('id'))
    except Device.ObjectDoesNotExist:
        return HttpResponse('Could not find device.', status=404)

    try:
        updated_device = DeviceAPIForm(request.POST, instance=device)
    except:
        print("Could not fill modelform with data")
        traceback.print_exception()

    updated_device.save()

    return HttpResponse(status=200)


@device_call
def register_device(request):
    
    if not verify_request(request):
        return HttpResponse('Request could not be verified, make sure your information is correct.', status=401)

    device_data = {
        'ip': request.META.get('remote_addr'),
        'device_id': secrets.token_urlsafe(32),
        'user': User.objects.get(username=request.POST.get('user'))
    }
    device = DeviceAPIForm(request.POST, initial=device_data)
    device.save()

    return HttpResponse(status=200)