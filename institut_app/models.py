from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    adresse = models.CharField(max_length=100, null=True, blank=True)

class Formation(models.Model):
    nom = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    duree = models.PositiveIntegerField()
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom

class Etudiant(models.Model):
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=15, null=True, blank=True)
    date_inscription = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.prenom} {self.nom}"