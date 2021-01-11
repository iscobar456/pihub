from django import forms
from dashboard.models import Device
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404


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
    current_password = forms.CharField(required=False)
    password = forms.CharField(required=False)
    password_confirm = forms.CharField(required=False)

    bio = forms.CharField(required=False)
    picture = forms.ImageField(required=False)
    

    user = None

    def clean(self):
        cleaned_data = super().clean()

        username = cleaned_data.get('username')
        self.user = get_object_or_404(User, id=cleaned_data.get('user_id'))
        existing_user = User.objects.filter(username=username).exclude(id=self.user.id)
        if existing_user:
            self.add_error('username', 'Username already taken.')

        current_password = cleaned_data.get('current_password')
        new_password = cleaned_data.get('password')
        new_password_confirm = cleaned_data.get('password_confirm')

        if current_password or new_password or new_password_confirm:
            if current_password:
                if not check_password(current_password, self.user.password):
                    self.add_error('current_password', "The entered password is incorrect.")
            else:
                self.add_error('current_password', "This field must be filled out to change the password.")

            if not new_password:
                self.add_error('password', "This field must be filled out to change the password.")

            if new_password_confirm:
                if new_password != new_password_confirm:
                    self.add_error('password_confirm', "The passwords do not match")
            else:
                raise self.add_error('password', "This field must be filled out to change the password.")


    
class UpdateNotesForm(forms.Form):
    device_id = forms.CharField()
    notes = forms.CharField(max_length=2048)
    markdown_enabled = forms.BooleanField()

    def clean(self):
        cleaned_data = super().clean()
        self.device = get_object_or_404(Device, id=cleaned_data.get('device_id'))
