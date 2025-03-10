from django import forms
from .models import *

class NouveauEmploye(forms.ModelForm):
    class Meta:
        model = Employees
        fields = '__all__'
        exclude = ['has_contract','tenant','created_by','updated_by','created_at','updated_at']
        widgets = {
            'civilite' : forms.Select(attrs={'class' : 'form-control'}),
            'nom' : forms.TextInput(attrs={'class' : 'form-control'}),
            'prenom' : forms.TextInput(attrs={'class' : 'form-control'}),
            'email' : forms.TextInput(attrs={'class' : 'form-control'}),
            'telephone' : forms.TextInput(attrs={'class' : 'form-control'}),
            'adresse' : forms.TextInput(attrs={'class' : 'form-control'}),
            'cin' : forms.TextInput(attrs={'class' : 'form-control'}),
            'nin' : forms.TextInput(attrs={'class' : 'form-control'}),
            'secu' : forms.TextInput(attrs={'class' : 'form-control'}),
            'situation_familiale' : forms.Select(attrs={'class' : 'form-control'}),
            'sexe' : forms.Select(attrs={'class' : 'form-control'}),
            'date_naissance' : forms.TextInput(attrs={'class' : 'form-control', 'type' : 'date'}),
            'lieu_naissance' : forms.TextInput(attrs={'class' : 'form-control'}),
            'bank' : forms.TextInput(attrs={'class' : 'form-control'}),
        }
        labels = {
            'civilite' : "Civilité :",
            'nom' : "Nom :",
            'prenom' : "Prénom :",
            'email' : "Email :",
            'telephone' : "N° Téléphone :",
            'adresse' : "Adresse :",
            'cin' : "N° Carte Identite National :",
            'nin': "N° Identification National :",
            'secu' : "N° Sécurité Social :",
            'situation_familiale' : "Situation Famillial :",
            'sexe' : "Sexe :",
            'date_naissance' : "Date de naissance :",
            'lieu_naissance' : "Lieu de naissance :",
            'bank' : "N° compte bancaire :",
        }

class NouveauService(forms.ModelForm):
    class Meta:
        model = Services
        fields = '__all__'
        exclude = ['created_by','created_at','updated_at']

class NouvelleArticleContrat(forms.ModelForm):
    class Meta:
        model = ArticlesContrat
        fields = '__all__'
        exclude = ['created_by','created_at','updated_at']