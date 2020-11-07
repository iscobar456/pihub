from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_POST

# Create your views here.

@require_POST
def update_ip(request):
    
    return HttpResponse(status=200)