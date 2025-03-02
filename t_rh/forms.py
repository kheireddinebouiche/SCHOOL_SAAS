from django import forms
from .models import *

class NouveauEmploye(forms.ModelForm):
    class Meta:
        model = Employees
        fields = '__all__'
        exclude = ['tenant','created_by','updated_by','created_at','updated_at']


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