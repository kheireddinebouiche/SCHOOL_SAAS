from django import forms
from .models import *

class NewFormationForm(forms.ModelForm):
    class Meta:
        model = Formation
        fields = ['entite_legal','nom', 'description', 'duree','frais_inscription','frais_assurance']

        widgets = {
            'nom' : forms.TextInput(attrs={'class':'form-control'}),
            'description': forms.Textarea(attrs={'class':'form-control'}),
            'duree' : forms.TextInput(attrs={'class':'form-control', 'type' : 'number', 'placeholder' : "Durée de total de la formation stage inclus (en mois)"}),
            'type_formation': forms.Select(attrs={'class': 'form-control'}),
            'frais_inscription' : forms.TextInput(attrs={'class' : 'form-control'}),
            'frais_assurance' : forms.TextInput(attrs={'class' : 'form-control'}),
            'entite_legal' : forms.Select(attrs={'class' : 'form-control'}),
        }

        labels = {
            'nom' : "Nom de la formation",
            'description' : "Description de la formation",
            'duree' : "Durée de la formation",
            'partenaire' : "Partenaire",
            'type_formation' : "Type de formation",
            'frais_inscription' : "Frais d'inscription",
            'frais_assurance' : "Frais d'assurance",
        }
        
class NewFormationFormMaster(forms.ModelForm):
    class Meta:
        model = Formation
        fields = ['nom', 'description', 'duree','partenaire','type_formation','frais_inscription','frais_assurance']
        widgets = {
            'nom' : forms.TextInput(attrs={'class':'form-control'}),
            'description': forms.Textarea(attrs={'class':'form-control'}),
            'duree' : forms.TextInput(attrs={'class':'form-control', 'type' : 'number', 'placeholder' : "Durée de total de la formation stage inclus (en mois)"}),
            'partenaire': forms.Select(attrs={'class': 'form-control'}),
            'type_formation': forms.Select(attrs={'class': 'form-control'}),
            'frais_inscription' : forms.TextInput(attrs={'class' : 'form-control'}),
            'frais_assurance' : forms.TextInput(attrs={'class' : 'form-control'}),
        }

        labels = {
            'nom' : "Nom de la formation",
            'description' : "Description de la formation",
            'duree' : "Durée de la formation",
            'partenaire' : "Partenaire",
            'type_formation' : "Type de formation",
            'frais_inscription' : "Frais d'inscription",
            'frais_assurance' : "Frais d'assurance",
        }

class NewPartenaireForm(forms.ModelForm):
    class Meta:
        model = Partenaires
        fields = "__all__"
        widgets = {
            'tenant': forms.HiddenInput(),
            'created_by': forms.HiddenInput(),
            'nom':  forms.TextInput(attrs={'class': 'form-control'}),
            'adresse' : forms.TextInput(attrs={'class': 'form-control'}),
            'code' : forms.TextInput(attrs={'class': 'form-control'}),
            'telephone':  forms.TextInput(attrs={'class': 'form-control'}),
            'email' : forms.TextInput(attrs={'class': 'form-control'}),
            'site_web' : forms.TextInput(attrs={'class': 'form-control'}),
           
        }

class NewSpecialiteForm(forms.ModelForm):
    class Meta:
        model = Specialites
        fields = ['code', 'label', 'prix', 'formation','duree','responsable','nb_semestre','version']

        widgets = {
            'code' : forms.TextInput(attrs={'class' : 'form-control'}),
            'label' : forms.TextInput(attrs={'class' : 'form-control'}),
            'prix' : forms.TextInput(attrs={'class' : 'form-control'}),
            'formation' : forms.Select(attrs={'class' : 'form-control'}),
            'duree' : forms.TextInput(attrs={'class' : 'form-control'}),
            'responsable' : forms.Select(attrs={'class':'form-control'}),
            'nb_semestre' : forms.Select(attrs={'class':'form-control'}),
            'version' : forms.TextInput(attrs={'class' : 'form-control'}),
        }

        labels = {
            'label' : "Désignation de la spécialité :",
            'code' : "Code la spécialité :",
            'formation' : "Formation parante :",
            'duree' : "Durée total de la formation (Stage inclue) ",
            'responsable' : "Responsable de spécialité :",
            'nb_semestre' : "Nombre de semestre théorique :",
            'version' : "Version du programme :",
        }

        def clean_name(self):
            name = self.cleaned_data.get("code")
            if Specialites.objects.filter(code=name).exists():
                raise forms.ValidationError("Cette spécialité existe déjà")
            return name

class NewModuleForm(forms.ModelForm):
    class Meta:
        model = Modules
        fields = ['specialite', 'code', 'label', 'duree', 'coef', 'n_elimate']

class NewFraisInscriptionForm(forms.ModelForm):
    class Meta:
        model = FraisInscription
        fields = ['specialite', 'label', 'montant']
