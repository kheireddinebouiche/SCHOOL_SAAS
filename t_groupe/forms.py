from django import forms
from .models import Groupe, GroupeLine


class NewGroupeForms(forms.ModelForm):
    class Meta:
        model = Groupe
        fields = "__all__"
        exclude = {
            'createdy',
            'etat',
        }

        widgets = {
            'start_date' : forms.DateInput(attrs={'class': 'form-control' ,'type':'date', 'id' : '_date_debut'}),
            'end_date' : forms.DateInput(attrs={'class': 'form-control' ,'type':'date', 'id' : '_date_fin'}),
            'nom' : forms.TextInput(attrs={'class': 'form-control'}),
            'description' : forms.Textarea(attrs={'class': 'form-control'}),
            'min_student' : forms.TextInput(attrs={'class' : 'form-control' , 'type' : 'number'}),
            'max_student' : forms.TextInput(attrs={'class' : 'form-control' , 'type' : 'number'}),
            'specialite' : forms.Select(attrs={'class' : 'form-control'}),
            'annee_scolaire' : forms.TextInput(attrs={'class' : 'form-control', 'id' : '_annee_scolaire', 'placeholder' : 'Ex: 2020/2021'}),
            'promotion' : forms.Select(attrs={'class' : 'form-control'}),
        }

        labels = {
            'start_date' : "Date de début de formation :",
            'end_date' : "Date de fin de formation :",
            'nom' : "Désignation (Nom du groupe ex: BTS Base de données): ",
            'description' : "Description courte de la formation :",
            'min_student' : "Minimum d'étudiants pour démarrer la formation :",
            'max_student' : "Maximum d'étudiants pour cloturer la formation :",
            'specialite' : "Spécialité :",
            'annee_scolaire' : "Année scolaire :",
            'promotion' : "Veuillez sélectionner la promo :",
        }

