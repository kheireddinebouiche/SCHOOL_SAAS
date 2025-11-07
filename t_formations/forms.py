from django import forms
from .models import *

class NewFormationForm(forms.ModelForm):
    class Meta:
        model = Formation
        fields = ['entite_legal','code','nom', 'partenaire','description','type_formation','duree','frais_inscription','prix_formation']

        widgets = {
            'nom' : forms.TextInput(attrs={'class':'form-control'}),
            'description': forms.Textarea(attrs={'class':'form-control'}),
            'duree' : forms.TextInput(attrs={'class':'form-control', 'type' : 'number', 'placeholder' : "Durée de total de la formation stage inclus (en mois)"}),
            'type_formation': forms.Select(attrs={'class': 'form-control'}),
            'frais_inscription' : forms.TextInput(attrs={'class' : 'form-control'}),
            'entite_legal' : forms.Select(attrs={'class' : 'form-control'}),
            'partenaire' : forms.Select(attrs={'class' : 'form-control'}),
            'code' : forms.TextInput(attrs={'class' : 'form-control'}),
            'type_formation' : forms.Select(attrs={'class' : 'form-control'}),
            'prix_formation' : forms.TextInput(attrs={'class' : 'form-control'}),
        }

        labels = {
            'nom' : "Nom de la formation",
            'description' : "Description de la formation",
            'duree' : "Durée de la formation",
            'partenaire' : "Partenaire",
            'type_formation' : "Type de formation",
            'frais_inscription' : "Frais d'inscription",
            'code' : 'Code de la formation',
            'type_formation' : "Type de formation",
            'prix_formation' : "Prix de la formation",
        }
        
class NewFormationFormMaster(forms.ModelForm):
    class Meta:
        model = Formation
        fields = ['qualification','entite_legal','code','nom', 'description', 'duree','partenaire','type_formation','frais_inscription','prix_formation']
        widgets = {
            'entite_legal' : forms.Select(attrs={'class' : 'form-control'}),
            'code' : forms.TextInput(attrs={'class' : 'form-control', 'id' : 'formationId'}),
            'nom' : forms.TextInput(attrs={'class':'form-control'}),
            'description': forms.Textarea(attrs={'class':'form-control'}),
            'duree' : forms.TextInput(attrs={'class':'form-control', 'type' : 'number', 'placeholder' : "Durée de total de la formation stage inclus (en mois)"}),
            'partenaire' : forms.Select(attrs={'class':'form-control'}),
            'type_formation': forms.Select(attrs={'class': 'form-control'}),
            'frais_inscription' : forms.TextInput(attrs={'class' : 'form-control'}),
            'prix_formation' : forms.TextInput(attrs={'class':'form-control','placeholder' : "EX : 1200,00"}),
            'qualification' : forms.TextInput(attrs={'class' : 'form-control', 'id' : 'qualificationId'}),
        }

        labels = {
            'nom' : "Nom de la formation",
            'code':  "Code de la formation",
            'description' : "Description de la formation",
            'duree' : "Durée de la formation",
            'partenaire' : "Partenaire",
            'type_formation' : "Type de formation",
            'frais_inscription' : "Frais d'inscription",
            'prix_formation' : "Prix de la formation",
            'qualification' : "Qualification :"
        }
    def __init__(self, *args, **kwargs):
        current_tenant = kwargs.pop('current_tenant', None)
        super().__init__(*args, **kwargs)

        if current_tenant:
            if current_tenant.tenant_type == "second":
                self.fields['type_formation'].choices = [
                    ('national', 'Formation Etatique')
                ]
                
                self.fields['partenaire'].queryset = Partenaires.objects.filter(
                    type_partenaire="national",
                    etat="active"
                )
            elif current_tenant.tenant_type == "master":
                self.fields['type_formation'].choices = [
                    ('national', 'Formation Etatique'),
                    ('etrangere', 'Formation étrangere')
                ]
                
                self.fields['partenaire'].queryset = Partenaires.objects.filter(
                    etat="active"
                )

class NewDossierInscriptionForm(forms.ModelForm):
    pass

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
            'observation' : forms.Textarea(attrs={'class': 'form-control','rows' : "3"}),
            'logo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
           
        }
        exclude = ['updated_by']

    def __init__(self, *args, **kwargs):
        current_tenant = kwargs.pop('current_tenant', None)  # récupère le tenant passé
        super().__init__(*args, **kwargs)

        if current_tenant:
            if current_tenant.tenant_type == "second":
                self.fields['type_partenaire'].choices = [
                    ('national', 'Partenaire National')
                ]
            elif current_tenant.tenant_type == "master":
                self.fields['type_partenaire'].choices = [
                    ('national', 'Partenaire National'),
                    ('etranger', 'Partenaire Etranger')
                ]

class NewSpecialiteForm(forms.ModelForm):
    class Meta:
        model = Specialites
        fields = ['abr','code', 'label', 'prix', 'formation','duree','responsable','nb_semestre','version','condition_access']

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
            'abr' : forms.TextInput(attrs={"class":"form-control"}),
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
            'abr' : "Abreviation :",
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
            'code' : forms.TextInput(attrs={"class" : 'form-control'}),
            'begin_year' : forms.TextInput(attrs={"class" : 'form-control', "placeholder": "Année",'id' : "begin_year_id"}),
            'end_year': forms.TextInput(attrs={"class": "form-control", "placeholder": "Année",'id' : "end_year_id"}),
            'date_debut' : forms.DateInput(attrs={'class' : 'form-control', 'type' : 'date', 'id' : "id_date_debut"}),
            'date_fin' : forms.DateInput(attrs={'class' : 'form-control', 'type' : 'date', 'id' : "id_date_fin"}),
        }

        labels = {
            'label' : "Nom d'affichage :",
            'session' : "Rentrée :",
            'code' : "Code Unique :",
            'begin_year' : "Année de début",
            'end_year' : "Année de fin",
            'date_debut' : "Date de lançement",
            'date_fin' : "Date de fin de formation",
        }