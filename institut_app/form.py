from  django import forms

class UserForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField()

class ProfilForm(forms.Form):
    adresse = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Veuillez saisir l\'adresse.'}))