from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.views import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.http import HttpResponse, Http404, HttpResponseRedirect
from home.model_forms import UserForm
from dashboard.forms import EditAccountForm, DeviceForm, UpdateNotesForm
from dashboard.models import Device, SocialConnection
from django.contrib.auth.models import User
import json
import secrets
import traceback

# Create your views here.

@login_required
def index(request):

    devices = Device.objects.filter(owner=request.user)

    context = {
        'devices': devices
    }
    return render(request, 'dashboard/index.html')


@login_required
def social(request):
    user = request.user
    connections = SocialConnection.objects.filter(connectees=user)
    friends = list(map(lambda connection : connection.connectees.exclude(id=user.id).first(), connections))
    print(friends)
    context = {
        'friends': friends,
    }
    return render(request, 'dashboard/social.html', context)


@login_required
def remove_friend(request, friend_id):
    try:
        user = request.user
        connections = SocialConnection.objects.filter(connectees=user).filter(connectees=friend_id)
        connections.delete()
        return HttpResponseRedirect("/dashboard/social")
    except:
        traceback.print_exc()
        return HttpResponse(status=500)


@login_required
@require_POST
def add_friend(request):
    try:
        user = request.user
        friend = get_object_or_404(User, username=request.POST.get("friend"))
        if not SocialConnection.objects.filter(conn_type="FR").filter(connectees=user).filter(connectees=friend):
            connection = SocialConnection()
            connection.save()
            connection.connectees.add(user)
            connection.connectees.add(friend)
            connection.save()
            return HttpResponse()
        else:
            return HttpResponse("Already friends with this user.", status=400)
    except Http404:
        return HttpResponse("Could not find user.", status=400)
    except:
        traceback.print_exc()
        return HttpResponse("Could not find user.", status=500)


def get_profile_card(request, friend_id):
    return render(request, "dashboard/profile-card.html", context={"user": get_object_or_404(User, id=friend_id)})

@login_required
def personal(request, action=None):
    devices = Device.objects.filter(owner=request.user)
    context = {
        'devices': devices,
        'new_device_form': DeviceForm(),
        'has_errors': 'no'
    }

    def add_device():
        form = DeviceForm(request.POST)

        try:
            device = form.save(commit=False)
            device.owner = request.user
            device.public_key = secrets.token_hex(16)
            device.private_key = secrets.token_hex(32)
            device.save()
        except:
            traceback.print_exc()
            context['has_errors'] = 'yes'
            context['new_device_form'] = form

        return render(request, 'dashboard/personal.html', context)


    def get_keys():
        device = get_object_or_404(Device, id=request.GET.get('d'))
        response = json.dumps({
            'name': device.name,
            'keys': {
                'public': device.public_key,
                'private': device.private_key
            }
        })
        return HttpResponse(response)

    if action == 'add-device' and request.method == "POST":
        return add_device()
    elif action == 'get-keys':
        return get_keys()

    return render(request, 'dashboard/personal.html', context)


@require_POST
def update_notes(request):
    form = UpdateNotesForm(request.POST)
    if form.is_valid():
        form.device.notes = form.cleaned_data.get('notes')
        form.device.markdown_enabled = form.cleaned_data.get('markdown_enabled')
        form.device.save()
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=400)

@method_decorator(login_required, name='dispatch')
class Account(View):

    def get(self, request):
        form = EditAccountForm()
        context = {
            'form': form,
            'success': False,
            'saving_error': False
        }
        return render(request, 'dashboard/account.html', context)

    def post(self, request):
        print("check 1")
        form = EditAccountForm(request.POST, request.FILES)
        context = {
            'user': request.user,
            'form': form,
            'success': False,
            'saving_error': False
        }
        if form.is_valid():
            print("check 2")
            try:
                user = form.user
                user.first_name = form.cleaned_data.get('first_name')
                user.last_name = form.cleaned_data.get('last_name')
                user.username = form.cleaned_data.get('username')
                user.email = form.cleaned_data.get('email')
                if form.cleaned_data.get('password'):
                    user.set_password(form.cleaned_data.get('password'))
                user.save()

                profile = user.profile
                profile.bio = form.cleaned_data.get('bio')
                if form.files.get("picture"):
                    profile.picture = form.files.get("picture")
                profile.save()

                context['success'] = True
                context['user'] = user
            except:
                traceback.print_exc()
                context['saving_error'] = True
        
        return render(request, 'dashboard/account.html', context)

