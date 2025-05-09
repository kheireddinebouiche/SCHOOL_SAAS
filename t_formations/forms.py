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
        fields = ['entite_legal','code','nom', 'description', 'duree','partenaire','type_formation','frais_inscription','frais_assurance']
        widgets = {
            'entite_legal' : forms.Select(attrs={'class' : 'form-control'}),
            'code' : forms.TextInput(attrs={'class' : 'form-control', 'id' : 'formationId'}),
            'nom' : forms.TextInput(attrs={'class':'form-control'}),
            'description': forms.Textarea(attrs={'class':'form-control'}),
            'duree' : forms.TextInput(attrs={'class':'form-control', 'type' : 'number', 'placeholder' : "Durée de total de la formation stage inclus (en mois)"}),
            'partenaire' : forms.Select(attrs={'class':'form-control'}),
            'type_formation': forms.Select(attrs={'class': 'form-control'}),
            'frais_inscription' : forms.TextInput(attrs={'class' : 'form-control'}),
            'frais_assurance' : forms.TextInput(attrs={'class' : 'form-control'}),
        }

        labels = {
            'nom' : "Nom de la formation",
            'code':  "Code de la formation",
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
            'type_partenaire' : forms.Select(attrs={'class':'form-control'}),
            'nom':  forms.TextInput(attrs={'class': 'form-control'}),
            'adresse' : forms.TextInput(attrs={'class': 'form-control'}),
            'code' : forms.TextInput(attrs={'class': 'form-control'}),
            'telephone':  forms.TextInput(attrs={'class': 'form-control'}),
            'email' : forms.TextInput(attrs={'class': 'form-control'}),
            'site_web' : forms.TextInput(attrs={'class': 'form-control'}),
        }
        exclude = ['updated_by']

class NewSpecialiteForm(forms.ModelForm):
    class Meta:
        model = Specialites
        fields = ['code', 'label', 'prix', 'formation','duree','responsable','nb_semestre','version','condition_access','dossier_inscription']

        widgets = {
            'code' : forms.TextInput(attrs={'class' : 'form-control', 'id' : 'specialiteId'}),
            'label' : forms.TextInput(attrs={'class' : 'form-control'}),
            'prix' : forms.TextInput(attrs={'class' : 'form-control'}),
            'formation' : forms.Select(attrs={'class' : 'form-control'}),
            'duree' : forms.TextInput(attrs={'class' : 'form-control'}),
            'responsable' : forms.Select(attrs={'class':'form-control'}),
            'nb_semestre' : forms.Select(attrs={'class':'form-control'}),
            'version' : forms.TextInput(attrs={'class' : 'form-control'}),
            'condition_access' : forms.TextInput(attrs={'class' : 'form-control'}),
            'dossier_inscription' : forms.Textarea(attrs={'class' : 'form-control'}),
        }

        labels = {
            'label' : "Désignation de la spécialité :",
            'code' : "Code la spécialité :",
            'formation' : "Formation parante :",
            'duree' : "Durée total de la formation (Stage inclue) ",
            'responsable' : "Responsable de spécialité :",
            'nb_semestre' : "Nombre de semestre théorique :",
            'version' : "Version du programme :",
            'condition_access' : "Conditions d'accès :",
            'dossier_inscription' : "Dossier d'inscription :",
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

class PromoForm(forms.ModelForm):
    class Meta:
        model = Promos
        fields = '__all__'
        exclude = ['created_by', 'created_at', 'updated_at','etat']
        widgets = {
            'label' : forms.TextInput(attrs={'class' : 'form-control'}),
            'session' : forms.Select(attrs={'class' : 'form-control'}),
        }