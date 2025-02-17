from django.db import models
from django.contrib.auth.models import User
from t_formations.models import *

class NouveauVisiteur(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    nom = models.CharField(max_length=255, null=True, blank=True)
    prenom = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    telephone = models.CharField(max_length=15, null=True, blank=True)
    adresse = models.TextField(null=True, blank=True)

    type_visiteur = models.CharField(max_length=255, null=True, blank=True, choices=[('particulier', 'Particulier'), ('entreprise', 'Entreprise')])

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    has_paied = models.BooleanField(default=False)

    cin = models.CharField(max_length=255, null=True, blank=True)

    formation = models.ForeignKey(Formation, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name="Visiteur"
        verbose_name_plural = "Visiteurs"

    def __str__(self):
        return f"{self.nom} {self.prenom}"
    

