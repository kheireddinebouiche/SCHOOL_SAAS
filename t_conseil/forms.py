from django import forms
from .models import *

class NewDevisForms(forms.ModelForm):
    class Meta:
        model = Devis
        fields = '__all__'
        exclude = ['num_devis','montant','etat']

        widgets = {
            'date_emission': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_echeance': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'client' : forms.Select(attrs={"class" : "form-control"}),
        }

        labels = {
            'date_emission' : "Date du devis",
            'date_echeance' : "Validité du devis",
            'client' : "Client" ,
        }
    def __init__(self, *args, **kwargs):
        super(NewDevisForms, self).__init__(*args, **kwargs)
        self.fields['client'].queryset = Prospets.objects.filter(type_prospect='entreprise')
    
                
                

        