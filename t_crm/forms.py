from  django import forms
from .models import *


class VisiteurForm(forms.ModelForm):
    class Meta:
        model = Visiteurs
        fields = '__all__'
        exclude = ['created_by','created_at','updated_at','has_paied']

        widgets = {

            'pays' : forms.Select(attrs={'class':'form-control'}),
        }