from django.db import models
from t_etudiants.models import *


class Stagiaire(models.Model):
    student = models.ForeignKey(Etudiant, on_delete=models.CASCADE)

    class meta:
        verbose_name = "Stagiaire"
        verbose_name_plural = "Stagiaires"

    def __str__(self):
        return f"{self.student}"
