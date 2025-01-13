from django import forms
from .models import UpdateInfo

class updateInfoForm(forms.ModelForm):
    class Meta:
        model = UpdateInfo
        fields = "__all__"