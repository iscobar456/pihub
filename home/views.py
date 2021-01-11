from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from home.forms import LoginForm
from home.model_forms import UserForm
from dashboard.models import Profile

# Create your views here.

def homepage(request):

    context = {

    }
    return render(request, 'index.html', context)

class Login(View):
    def get(self, request):

        context = {
            'form': LoginForm()
        }
        return render(request, 'login.html', context)
    
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user:
                login(request, user)
                return HttpResponseRedirect('/dashboard')
            else:
                context = {
                    'form': form,
                    'no_user_found': True
                }
        else:
            context = {
                'form': form,
                'no_user_found': False
            }
        return render(request, 'login.html', context)

class Register(View):
    
    def get(self, request):
        context = {
            'form': UserForm()
        }
        return render(request, 'register.html', context)
    
    def post(self, request):
        context = {
            'form': UserForm()
        }

        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            p = Profile(user=user)
            p.save()
            login(request, user)
            return HttpResponseRedirect('/dashboard')
        else:
            errors = form.errors
            context['form'] = form
            return render(request, 'register.html', context)
