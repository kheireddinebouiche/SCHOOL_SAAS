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
            'label' : "Nom du modèle :",
            'formation' : "Veuillez sélectionner la formation :",
            'is_default' : "Définir par défaut ? :",
        }

        widgets = {
            'label' : forms.TextInput(attrs={'class' : 'form-control'}),
            'formation' : forms.Select(attrs={'class' : 'form-control'}),
            'is_default' : forms.CheckboxInput(attrs={'class' : 'form-check-input'}),
        }

class CommissionForm(forms.ModelForm):
    class Meta:
        model = Commissions
        fields = "__all__"
        exclude = ['created_at', 'updated_at']

        widgets = {
            'label': forms.TextInput(attrs={'class': 'form-control'}),
            'promo': forms.Select(attrs={'class': 'form-control'}),
            'criters': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'date_commission': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_validated': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'participant': forms.SelectMultiple(attrs={'class': 'form-control select2-multiple-participants', 'multiple': 'multiple'}),
            'formateurs': forms.SelectMultiple(attrs={'class': 'form-control select2-multiple-formateurs', 'multiple': 'multiple'}),
            'groupes': forms.SelectMultiple(attrs={'class': 'form-control select2-multiple-groupes', 'multiple': 'multiple'}),
        }

        labels = {
            'label': 'Nom de la commission',
            'promo': 'Promotion',
            'criters': 'Critères',
            'date_commission': 'Date de la commission',
            'is_validated': 'Validée ?',
            'participant': 'Participants',
            'formateurs' : 'Formateurs',
            'groupes': 'Groupes concernés',
        }
