from django.forms import ModelForm
from dashboard.models import Device

class DeviceAPIForm(ModelForm):
    class Meta:
        model = Device
        fields = ['hostname']

class DeviceForm(ModelForm):
    class Meta:
        model = Device
        exclude = ['ip', 'owner', '']