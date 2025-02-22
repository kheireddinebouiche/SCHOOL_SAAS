from django import forms
from .models import *

class NewFormationForm(forms.ModelForm):
    class Meta:
        model = Formation
        fields = ['nom', 'description', 'duree','frais_inscription']

class NewFormationFormMaster(forms.ModelForm):
    class Meta:
        model = Formation
        fields = ['nom', 'description', 'duree','partenaire','type_formation','frais_inscription']
        widgets = {
            'nom' : forms.TextInput(attrs={'class':'form-control'}),
            'description': forms.Textarea(attrs={'class':'form-control'}),
            'duree' : forms.TextInput(attrs={'class':'form-control', 'type' : 'number', 'placeholder' : "Durée de total de la formation stage inclus (en mois)"}),
            'partenaire': forms.Select(attrs={'class': 'form-control'}),
            'type_formation': forms.Select(attrs={'class': 'form-control'}),
            'frais_inscription' : forms.TextInput(attrs={'class' : 'form-control'}),
        }

        labels = {
            'nom' : "Nom de la formation",
            'description' : "Description de la formation",
            'duree' : "Durée de la formation",
            'partenaire' : "Partenaire",
            'type_formation' : "Type de formation",
            'frais_inscription' : "Frais d'inscription",
        }

class NewPartenaireForm(forms.ModelForm):
    class Meta:
        model = Partenaires
        fields = "__all__"
        widgets = {
            'tenant': forms.HiddenInput(),
            'created_by': forms.HiddenInput(),

            'nom':  forms.TextInput(attrs={'class': 'form-control'})
,           'adresse' : forms.TextInput(attrs={'class': 'form-control'}),
            'code' : forms.TextInput(attrs={'class': 'form-control'}),
            'telephone':  forms.TextInput(attrs={'class': 'form-control'}),
            'email' : forms.TextInput(attrs={'class': 'form-control'}),
            'site_web' : forms.TextInput(attrs={'class': 'form-control'}),
           
        }

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
