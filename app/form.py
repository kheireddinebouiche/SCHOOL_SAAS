from django import forms
from .models import *

class NewTenantForm(forms.ModelForm):
    class Meta:
        model = Institut
        fields = ['nom','adresse','telephone']


class NewUser(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())