from django.db import models
from django.contrib.auth.models import User
from t_formations.models import *
from django_countries.fields import CountryField



class Visiteurs(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    civilite = models.CharField(max_length=255, null=True, choices=[('monsieur', 'Monsieur'), ('madame', 'Madame')])
    nom = models.CharField(max_length=255, null=True)
    prenom = models.CharField(max_length=255, null=True)
    date_naissance = models.DateField(null=True)
    lieu_naissance = models.CharField(max_length=255, null=True)

    email = models.EmailField(null=True)
    telephone = models.CharField(max_length=15, null=True)

    adresse = models.TextField(null=True)
    pays = CountryField(null=True)

    type_visiteur = models.CharField(max_length=255, null=True, choices=[('particulier', 'Particulier'), ('entreprise', 'Entreprise')])

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    has_paied_enrollment = models.BooleanField(default=False)
    has_completed_documents = models.BooleanField(default=False)
    has_paid_fees = models.BooleanField(default=False)

    cin = models.CharField(max_length=255, null=True, blank=True)

    niveau_etude = models.CharField(max_length=255, null=True, blank=True, choices=[('9af','9 AF/ 4 AM'),('1as','1 AS/2 AS'),('ter','Terminal'),('bac', 'Bac'), ('bac+2', 'Bac+2'), ('bac+3', 'Bac+3'), ('bac+4', 'Bac+4'), ('bac+5', 'Bac+5')])

    situation_family = models.CharField(max_length=255, null=True, blank=True, choices=[('celibataire', 'Célibataire'), ('marie', 'Marié(e)')])
    situation_professionnelle = models.CharField(max_length=255, null=True, blank=True, choices=[('etudiant', 'Etudiant(e)'), ('salarié', 'Salarié(e)'), ('employeur', 'Employeur'),('sans_emploi', 'Sans emploi')])
    post_occupe = models.CharField(max_length=255, null=True, blank=True)
    experience = models.CharField(max_length=255, null=True, blank=True)
    entreprise = models.CharField(max_length=255, null=True, blank=True)

    is_student = models.BooleanField(default=False)
    is_entreprise = models.BooleanField(default=False)

    etat = models.CharField(max_length=255, null=True, blank=True, default='visiteur' , choices=[('visiteur','Visiteur'),('en_attente', 'En attente'), ('inscrit', 'Inscrit'), ('rejete', 'Rejeté')])
    
    class Meta:
        verbose_name="Visiteur"
        verbose_name_plural = "Visiteurs"

    def __str__(self):
        return f"{self.nom} {self.prenom}"
    
class DemandeInscription(models.Model):

    visiteur = models.ForeignKey(Visiteurs, on_delete=models.CASCADE, null=True, blank=True)

    formation = models.ForeignKey(Formation, on_delete=models.SET_NULL, null=True, blank=True)

    specialite = models.ForeignKey(Specialites, on_delete=models.SET_NULL, null=True, blank=True)

    promo = models.ForeignKey(Promos, on_delete=models.SET_NULL, null=True, blank=True, related_name="promo_demande_inscription", limit_choices_to={'etat':'active'})

    formule = models.CharField(max_length=255, null=True, blank=True, choices=[('week', 'Week-End'), ('jour', 'Cours du jour'), ('soir', 'Cours du soir')])
    session = models.CharField(max_length=255, null=True, blank=True, choices=[('octobre', 'Octobre'), ('mars', 'mars')])

    etat = models.CharField(max_length=255, null=True, blank=True, default='en_attente', choices=[('en_attente', 'En attente'), ('accepte', 'Accepté'), ('rejete', 'Rejeté')])

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,related_name="created_by_demande_inscription")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="updated_by_demande_inscription")

    class Meta:
        verbose_name="Demande d'inscription"
        verbose_name_plural = "Demandes d'inscription"

    def __str__(self):
        return f"{self.visiteur.nom} + {self.visiteur.prenom} - {self.specialite.label}"

