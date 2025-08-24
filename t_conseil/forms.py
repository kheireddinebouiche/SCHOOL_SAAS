from django import forms
from .models import *

class NewDevisForms(forms.ModelForm):
    class Meta:
        model = Devis
        fields = '__all__'
        exclude = ['num_devis']

        widgets = {
            'date_emission': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_echeance': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

        