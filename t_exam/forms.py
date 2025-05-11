from  django import forms
from .models import *


class SessionForm(forms.ModelForm):
    class Meta:
        model = SessionExam
        fields = "__all__"
        exclude = ['created_at','updated_at','updated_by']

        widgets = {
            'code' : forms.TextInput(attrs={'class' : 'form-control'}),
            'label':forms.TextInput(attrs={'class' : 'form-control'}),
            'type_session':forms.Select(attrs={'class' : 'form-control'}),
            'date_debut':forms.DateInput(attrs={'class' : 'form-control','type' :'date', 'id':'id_date_debut'}),
            'date_fin':forms.DateInput(attrs={'class' : 'form-control','type' :'date', 'id':'id_date_defin'}),
        }

class BuilltinForm(forms.ModelForm):
    class Meta:
        model = ModelBuilltins
        fields = "__all__"
        labels = {
            'label' : "Nom du modéle :",
            'formation' : "Veuillez séléctionner la formation :",
            'is_default' : "Définir par défaut ? :",
        }

        widgets = {
            'label' : forms.TextInput(attrs={'class' : 'form-control'}),
            'formation' : forms.Select(attrs={'class' : 'form-control'}),
            'is_default' : forms.CheckboxInput(attrs={'class' : 'form-check-input'}),
        }
