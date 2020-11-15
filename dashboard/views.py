from django.shortcuts import render
from django.contrib.auth.views import login_required
from django.utils.decorators import method_decorator
from home.model_forms import UserForm

# Create your views here.

@login_required
def index(request):

    context = {
        
    }
    return render(request, 'dashboard/index.html')


@login_required
def social(request):
    
    context = {
        
    }
    return render(request, 'dashboard/social.html')


@login_required
def personal(request):
    
    context = {
        
    }
    return render(request, 'dashboard/personal.html')


@login_required
def account(request):
    if request.method == 'POST':
        pass
    
    return render(request, 'dashboard/account.html')