from  django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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