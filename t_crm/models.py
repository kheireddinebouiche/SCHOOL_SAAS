from django.db import models
from django.contrib.auth.models import User
from t_formations.models import *
from django_countries.fields import CountryField



class Visiteurs(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    nom = models.CharField(max_length=255, null=True, blank=True)
    prenom = models.CharField(max_length=255, null=True, blank=True)
    date_naissance = models.DateField(null=True, blank=True)
    lieu_naissance = models.CharField(max_length=255, null=True, blank=True)

    email = models.EmailField(null=True, blank=True)
    telephone = models.CharField(max_length=15, null=True, blank=True)

    adresse = models.TextField(null=True, blank=True)
    pays = CountryField(null=True, blank=True)

    type_visiteur = models.CharField(max_length=255, null=True, blank=True, choices=[('particulier', 'Particulier'), ('entreprise', 'Entreprise')])

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    has_paied = models.BooleanField(default=False)

    cin = models.CharField(max_length=255, null=True, blank=True)

    niveau_etude = models.CharField(max_length=255, null=True, blank=True, choices=[('9af','9 AF/ 4 AM'),('1as','1 AS/2 AS'),('ter','Terminal'),('bac', 'Bac'), ('bac+2', 'Bac+2'), ('bac+3', 'Bac+3'), ('bac+4', 'Bac+4'), ('bac+5', 'Bac+5')])

    formule = models.CharField(max_length=255, null=True, blank=True, choices=[('week', 'Week-End'), ('jour', 'Cours du jour'), ('soir', 'Cours du soir')])
    session = models.CharField(max_length=255, null=True, blank=True, choices=[('octobre', 'Octobre'), ('mars', 'mars')])

    formation = models.ForeignKey(Formation, on_delete=models.SET_NULL, null=True, blank=True)

    situation_family = models.CharField(max_length=255, null=True, blank=True, choices=[('celibataire', 'Célibataire'), ('marie', 'Marié(e)')])
    situation_professionnelle = models.CharField(max_length=255, null=True, blank=True, choices=[('etudiant', 'Etudiant(e)'), ('salarié', 'Salarié(e)'), ('employeur', 'Employeur'),('sans_emploi', 'Sans emploi')])
    post_occupe = models.CharField(max_length=255, null=True, blank=True)
    experience = models.CharField(max_length=255, null=True, blank=True)
    entreprise = models.CharField(max_length=255, null=True, blank=True)
    
    class Meta:
        verbose_name="Visiteur"
        verbose_name_plural = "Visiteurs"

    def __str__(self):
        return f"{self.nom} {self.prenom}"
    

