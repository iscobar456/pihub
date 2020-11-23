from django import forms
from dashboard.models import Device
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404

class DeviceAPIForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['hostname']

class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = [
            'name',
            'description'
        ]


class EditAccountForm(forms.Form):
    """
    
    """
    first_name = forms.CharField()
    last_name = forms.CharField()
    username = forms.CharField()
    email = forms.EmailField()
    user_id = forms.IntegerField()
    current_password = forms.CharField(widget=forms.PasswordInput())
    password = forms.CharField(widget=forms.PasswordInput())
    password_confirm = forms.CharField(widget=forms.PasswordInput())

    user = None

    def clean(self):
        cleaned_data = super().clean()

        username = cleaned_data.get('username')
        self.user = get_object_or_404(User, id=cleaned_data.get('user_id'))
        existing_user = User.objects.filter(username=username).exclude(id=self.user.id)
        if existing_user:
            self.add_error('username', 'Username already taken.')
        else:
            return username

        current_password = cleaned_data.get('current_password')
        if check_password(password, self.user.password):
            return current_password
        else:
            self.add_error('current_password', 'The entered password is incorrect.')

        password = cleaned_data['password']
        if password == cleaned_data['password_confirm']:
            return password
        else:
            raise self.add_error('password', 'Passwords do not match')


    
