from django import forms
from dashboard.models import Device

class DeviceAPIForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['hostname']

class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        exclude = ['ip', 'owner', '']