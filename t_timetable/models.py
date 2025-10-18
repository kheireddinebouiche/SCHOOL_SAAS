from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime
from t_groupe.models import *
from t_formations.models import Modules

class Timetable(models.Model):
    """
    Main timetable model representing a schedule
    """
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
    cree_par = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.label} - {self.groupe.nom} - {self.semestre}"

    class Meta:
        verbose_name = "Emploi du temps"
        verbose_name_plural = "Emplois du temps"
        ordering = ['-date_creation']

class Salle(models.Model):
    """
    Represents a classroom or location where courses are held
    """
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

class Jour(models.Model):
    timetable = models.ForeignKey(Timetable, on_delete=models.CASCADE, null=True, blank=True)
    nom = models.CharField(max_length=20, verbose_name="Nom du jour")
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name = "Jour"
        verbose_name_plural = "Jours"
        
class Horaire(models.Model):
    """
    Represents a time slot that can be configured for a timetable
    """
    timetable = models.ForeignKey(Timetable, on_delete=models.CASCADE, null=True, blank=True)
    nom = models.CharField(max_length=50, verbose_name="Nom de l'horaire")
    heure_debut = models.TimeField(verbose_name="Heure de début")
    heure_fin = models.TimeField(verbose_name="Heure de fin")
    est_actif = models.BooleanField(default=True, verbose_name="Est actif")
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nom} ({self.heure_debut.strftime('%H:%M')}-{self.heure_fin.strftime('%H:%M')})"

    @property
    def duree(self):
        """Returns the duration of the time slot"""
        return self.heure_fin - self.heure_debut

    class Meta:
        verbose_name = "Horaire"
        verbose_name_plural = "Horaires"
        ordering = ['heure_debut']


class TimetableEntry(models.Model):
    """
    Represents a single entry in a timetable (a specific course at a specific time and place)
    """
    timetable = models.ForeignKey(Timetable, on_delete=models.CASCADE, verbose_name="Emploi du temps")
    cours = models.ForeignKey(Modules, on_delete=models.CASCADE, verbose_name="Cours")
    salle = models.ForeignKey(Salle, on_delete=models.CASCADE, verbose_name="Salle")
    jour = models.ForeignKey(Jour, on_delete=models.CASCADE, verbose_name="Jour")
    horaire = models.ForeignKey(Horaire, on_delete=models.CASCADE, verbose_name="Horaire")
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.cours.code} - {self.jour.nom} {self.horaire.nom} - {self.salle.code}"

    class Meta:
        verbose_name = "Entrée d'emploi du temps"
        verbose_name_plural = "Entrées d'emploi du temps"
        unique_together = ['timetable', 'jour', 'horaire']  # Prevents overlapping schedules
