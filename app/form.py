from django import forms
from .models import *

class NewTenantForm(forms.ModelForm):
    class Meta:
        model = Institut
        fields = ['nom','adresse','telephone']


