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
        'login_form': LoginForm(),
        'register_form': UserForm(),
    }
    return render(request, 'index.html', context)

class Login(View):
    def get(self, request):
        context = {
            'login_form': LoginForm(),
            'register_form': UserForm(),
        }
        return render(request, 'index.html', context)
    
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user:
                login(request, user)
                return HttpResponseRedirect('/dashboard')
            else:
                print("no user found")
                context = {
                    'login_form': LoginForm(),
                    'register_form': UserForm(),
                    'no_user_found': True
                }
        else:
            context = {
                'login_form': LoginForm(),
                'register_form': UserForm(),
                'no_user_found': False
            }
        return render(request, 'index.html', context)

class Register(View):
    
    def get(self, request):
        context = {
            'login_form': LoginForm(),
            'register_form': UserForm(),
            'focus_signup': True
        }
        return render(request, 'index.html', context)
    
    def post(self, request):
        context = {
            'login_form': LoginForm(),
            'register_form': UserForm(),
            'focus_signup': True
        }

        if request.POST.get('password') != request.POST.get('password_confirm'):
            context['different_passwords'] = True
            return render(request, 'index.html', context)

        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            p = Profile(user=user)
            p.save()
            login(request, user)
            return HttpResponseRedirect('/dashboard')
        else:
            print("form not valid")
            print(form.errors)
            context['register_form'] = form
            return render(request, 'index.html', context)
