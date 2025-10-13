from django.db import models
from django.contrib.auth.models import User
from t_formations.models import *
from t_crm.models import *


class Groupe(models.Model):
    createdy = models.ForeignKey(User, on_delete=models.CASCADE, related_name='groupe_createdy', null=True, blank=True)

    nom = models.CharField(max_length=100, null=True, blank=True)
    code_partenaire = models.CharField(max_length=100 ,null=True, blank=True)
    annee_scolaire = models.CharField(max_length=9, null=True, blank=True)
    promotion = models.ForeignKey(Promos, on_delete=models.DO_NOTHING, null=True)

    min_student = models.IntegerField(default=0, null=True, blank=True)
    max_student = models.IntegerField(default=0, null=True, blank=True)

    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    specialite = models.ForeignKey(Specialites, on_delete=models.CASCADE, related_name='groupe_specialite', null=True, blank=True)

    etat = models.CharField(max_length=200, choices=[('valider','Groupe valider'),('brouillon','Brouillon'),('inscription',"En cours d'inscription"),('enc', 'En cours'), ('cloture', 'Cloturé')], default='brouillon')

    date_creation = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nom} - {self.promotion}"
    
    class Meta:
        ordering = ['nom']


class GroupeLine(models.Model):
    groupe = models.ForeignKey(Groupe, on_delete=models.CASCADE, related_name='groupe_line_groupe')
    student = models.ForeignKey(Prospets, on_delete=models.CASCADE, related_name='groupe_line_student')

    date_inscription = models.DateTimeField(auto_now_add=True)
    date_sortie = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name="Groupe d'etudiants"
        verbose_name_plural = "Groupes d'etudiants"

    def __str__(self):
        return f"{self.groupe.nom} - {self.student.prenom} {self.student.nom}"