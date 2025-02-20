from django import forms
from .models import *

class NewFormationForm(forms.ModelForm):
    class Meta:
        model = Formation
        fields = ['nom', 'description', 'duree', 'entite_legal','partenaire']


class NewSpecialiteForm(forms.ModelForm):
    class Meta:
        model = Specialites
        fields = ['code', 'label', 'prix', 'duree', 'formation']

class NewModuleForm(forms.ModelForm):
    class Meta:
        model = Modules
        fields = ['specialite', 'code', 'label', 'duree', 'coef', 'n_elimate']

class NewFraisInscriptionForm(forms.ModelForm):
    class Meta:
        model = FraisInscription
        fields = ['specialite', 'label', 'montant']
