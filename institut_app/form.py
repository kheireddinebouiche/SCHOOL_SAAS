from  django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField()

class ProfilForm(forms.Form):
    adresse = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Veuillez saisir l\'adresse.'}))

class EntrepriseForm(forms.ModelForm):
    class Meta:
        model = Entreprise
        fields = ['designation', 'rc', 'nif', 'art', 'nis']

        labels = {
            'designation' : "Désignation :",
            'rc' : "N° Registre Commerce :",
            'nif' : "N° Identification Fiscale :",
            'art' : "N° Article :",
            'nis' : "N° Identification Statistique :"
        }

        widgets = {
            'designation' : forms.TextInput(attrs={'class':'form-control'}),
            'rc' : forms.TextInput(attrs={'class':'form-control'}),
            'nif' : forms.TextInput(attrs={'class':'form-control'}),
            'art' : forms.TextInput(attrs={'class':'form-control'}),
            'nis' : forms.TextInput(attrs={'class':'form-control'})
        }