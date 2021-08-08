from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
# from home.models import 


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
        widgets = {
            'email': forms.EmailInput(),
            'password': forms.PasswordInput()
        }
    

    def clean_password(self):
        password = self.cleaned_data['password']
        password = make_password(password)
        return password

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email):
            raise forms.ValidationError("This email is already in use.")
        return email
