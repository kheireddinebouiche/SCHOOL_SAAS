from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime
from t_groupe.models import *
from t_formations.models import Modules

class Timetable(models.Model):
    
    label = models.CharField(max_length=200, verbose_name="Label")
    groupe = models.ForeignKey(Groupe, on_delete=models.CASCADE, verbose_name="Groupe")
    semestre = models.CharField(
        max_length=20,
        choices=[
            ('1', 'Semestre 1'),
            ('2', 'Semestre 2'),
            ('3', 'Semestre 3'),
            ('4', 'Semestre 4'),
        ],
        verbose_name="Semestre"
    )
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    est_actif = models.BooleanField(default=True, verbose_name="Est actif")
    is_configured = models.BooleanField(default=False)
    creneau = models.ForeignKey('ModelCrenau', on_delete=models.CASCADE, null=True, blank=True)
    cree_par = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.label} - {self.groupe.nom} - {self.semestre}"

    class Meta:
        verbose_name = "Emploi du temps"
        verbose_name_plural = "Emplois du temps"
        ordering = ['-date_creation']

class Salle(models.Model):
    
    nom = models.CharField(max_length=100, verbose_name="Nom de la salle")
    code = models.CharField(max_length=20, unique=True, verbose_name="Code de la salle")
    capacite = models.IntegerField(verbose_name="Capacité")
    type_salle = models.CharField(
        max_length=50,
        choices=[
            ('Amphi', 'Amphithéâtre'),
            ('TD', 'Travaux Dirigés'),
            ('TP', 'Travaux Pratiques'),
            ('Bureau', 'Bureau'),
        ],
        verbose_name="Type de salle"
    )
    equipements = models.TextField(blank=True, null=True, verbose_name="Équipements")
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nom} ({self.code})"

    class Meta:
        verbose_name = "Salle"
        verbose_name_plural = "Salles"
        ordering = ['nom']

class ModelCrenau(models.Model):
    label = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    jour_data = models.JSONField(default=dict, blank=True, null=True)
    horaire_data = models.JSONField(default=dict, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.label or "Créneau sans label"

    def set_jour(self, jour_obj):
        if jour_obj:
            self.jour_data = {
                "id": jour_obj.id,
                "nom": jour_obj.nom,
                "date_creation": jour_obj.date_creation.isoformat(),
            }

    def set_horaire(self, horaire_obj):
        if horaire_obj:
            self.horaire_data = {
                "id": horaire_obj.id,
                "nom": horaire_obj.nom,
                "heure_debut": horaire_obj.heure_debut.strftime("%H:%M"),
                "heure_fin": horaire_obj.heure_fin.strftime("%H:%M"),
                "est_actif": horaire_obj.est_actif,
            }

class TimetableEntry(models.Model):

    timetable = models.ForeignKey(Timetable, on_delete=models.CASCADE, verbose_name="Emploi du temps")
    cours = models.ForeignKey(Modules, on_delete=models.CASCADE, verbose_name="Cours")
    salle = models.ForeignKey(Salle, on_delete=models.CASCADE, verbose_name="Salle")
    crenau = models.ForeignKey(ModelCrenau, on_delete=models.CASCADE, null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.cours.code} - {self.jour.nom} {self.horaire.nom} - {self.salle.code}"

    class Meta:
        verbose_name = "Entrée d'emploi du temps"
        verbose_name_plural = "Entrées d'emploi du temps"
        unique_together = ['timetable','crenau']
