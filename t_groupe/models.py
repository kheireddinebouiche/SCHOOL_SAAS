from django.db import models
from django.contrib.auth.models import User
from t_formations.models import *
from t_etudiants.models import *


class Groupe(models.Model):
    createdy = models.ForeignKey(User, on_delete=models.CASCADE, related_name='groupe_createdy')

    nom = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(blank=True, null=True)

    annee_scolaire = models.CharField(max_length=9, null=True, blank=True)

    min_student = models.IntegerField(default=0)
    max_student = models.IntegerField(default=0)

    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    specialite = models.ForeignKey(Specialites, on_delete=models.CASCADE, related_name='groupe_specialite', null=True, blank=True)

    etat = models.CharField(max_length=200, choices=[('inscription',"En cours d'inscription"),('enc', 'En cours'), ('Cloturé', 'Cloturé')], default='inscription')

    date_creation = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom
    
    class Meta:
        ordering = ['nom']


class GroupeLine(models.Model):
    groupe = models.ForeignKey(Groupe, on_delete=models.CASCADE, related_name='groupe_line_groupe')
    student = models.ForeignKey(Etudiant, on_delete=models.CASCADE, related_name='groupe_line_student')

    date_inscription = models.DateTimeField(auto_now_add=True)
    date_sortie = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name="Groupe d'etudiants"
        verbose_name_plural = "Groupes d'etudiants"

    def __str__(self):
        return f"{self.groupe.nom} - {self.student.prenom} {self.student.nom}"