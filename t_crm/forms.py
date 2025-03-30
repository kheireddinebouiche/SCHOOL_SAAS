from  django import forms
from .models import *


class VisiteurForm(forms.ModelForm):
    class Meta:
        model = Visiteurs
        fields = '__all__'
        exclude = ['etat','created_by','created_at','updated_at','has_paied','has_paied_enrollment','has_completed_documents','has_paid_fees','is_student','is_entreprise']

        widgets = {

            'pays' : forms.Select(attrs={'class':'form-control', 'id':'pays'}),
            'civilite' : forms.Select(attrs={'class':'form-control','required':'True'}),
            'nom' : forms.TextInput(attrs={'class':'form-control'}),
            'prenom' : forms.TextInput(attrs={'class':'form-control'}),
            'date_naissance' : forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
            'lieu_naissance' : forms.TextInput(attrs={'class':'form-control'}),
            'email' : forms.EmailInput(attrs={'class':'form-control'}),
            'telephone' : forms.TextInput(attrs={'class':'form-control'}),
            'adresse' : forms.Textarea(attrs={'class':'form-control'}),
            'type_visiteur' : forms.Select(attrs={'class':'form-control'}),
            'cin' : forms.TextInput(attrs={'class':'form-control'}),
            'niveau_etude' : forms.Select(attrs={'class':'form-control'}),
            'situation_family' : forms.Select(attrs={'class':'form-control'}),
            'situation_professionnelle' : forms.Select(attrs={'class':'form-control'}),
            'post_occupe' : forms.TextInput(attrs={'class':'form-control'}),
            'experience' : forms.TextInput(attrs={'class':'form-control'}),
            'entreprise' : forms.TextInput(attrs={'class':'form-control'}),
            
        }

        labels = {
            'pays' : 'Pays',
            'nom' : 'Nom',
            'civilite' : 'Civilité',
            'prenom' : 'Prénom',
            'date_naissance' : 'Date de naissance',
            'lieu_naissance' : 'Lieu de naissance',
            'email' : 'Email',
            'telephone' : 'Téléphone',
            'adresse' : 'Adresse',
            'type_visiteur' : 'Type de visiteur',
            'cin' : 'CIN',
            'niveau_etude' : 'Niveau d\'étude',
            'formule' : 'Formule',
            'session' : 'Session',
            'formation' : 'Formation',
            'situation_family' : 'Situation familiale',
            'situation_professionnelle' : 'Situation professionnelle',
            'post_occupe' : 'Poste occupé',
            'experience' : 'Expérience',
            'entreprise' : 'Entreprise',
            'specialite' : 'Spécialité',
        }
    
    

class DemandeInscriptionForm(forms.ModelForm):
    
    class Meta:
        model = DemandeInscription
        fields = '__all__'
        exclude = ['created_at','updated_at','created_by','etat','updated_by','visiteur']

        widgets = {
            
            'formation' : forms.Select(attrs={'class':'form-control', 'id':'formation', }),
            'promo' : forms.Select(attrs={'class':'form-control'}),
            'formule' : forms.Select(attrs={'class':'form-control'}),
            'specialite' : forms.Select(attrs={'class':'form-control', 'id':'specialite'}),
            'session' : forms.Select(attrs={'class':'form-control'}),
        }

        labels = {
            'formation' : 'Formation',
            'specialite' : 'Spécialité',
            'promo' : 'Promotion',
            'formule' : 'Formule',
            'session' : 'Session',
        }

