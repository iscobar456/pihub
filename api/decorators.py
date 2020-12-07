from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from functools import wraps

def protected_endpoint(func):
    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            device = get_object_or_404(Device, public_key=request.POST.get('pubkey'))

            request_hash = hashlib.sha256()
            request_hash.update(request.POST.get('pubkey'))
            request_hash.update(request.POST.get('time'))
            request_hash.update(device.secret_key)
            hash_string = request_hash.hexdigest()

            if not hash_string == request.POST.get('verification'):
                return HttpResponse('Request could not be verified, make sure your information is correct.', status=401)
            return require_POST(csrf_exempt(func(request, *args, **kwargs)))
        return inner
    return decorator