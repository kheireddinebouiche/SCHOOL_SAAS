from django.db import models
from app.models import *


class Employees(models.Model):
    tenant = models.ForeignKey(Institut, on_delete=models.CASCADE, null=True, blank=True)
    nom = models.CharField(max_length=255, null=True, blank=True)
    prenom = models.CharField(max_length=255, null=True, blank=True)

    email = models.EmailField(null=True, blank=True)
    telephone = models.CharField(max_length=15, null=True, blank=True)

    adresse = models.TextField(null=True, blank=True)

    poste = models.CharField(max_length=255, null=True, blank=True, choices=[('emp','Employe(e)'), ('dir', 'Directeur(trice)'), ('per', 'Enseignant permanant'), ('vac', 'Enseignant vacataire')])
    
    salaire = models.DecimalField(max_digits=200, decimal_places=2, null=True, blank=True)
    date_embauche = models.DateField(null=True, blank=True)
    date_depart = models.DateField(null=True, blank=True)

    cin = models.CharField(max_length=255, null=True, blank=True)
    secu = models.CharField(max_length=255, null=True, blank=True) 

    situation_familiale = models.CharField(max_length=255, null=True, blank=True, choices=[('C', 'Célibataire'), ('M', 'Marié(e)'), ('D', 'Divorcé(e)'), ('V', 'Veuf(ve)')])
    sexe = models.CharField(max_length=1, null=True, blank=True, choices=[('M', 'Masculin'), ('F', 'Feminin')])
    date_naissance = models.DateField(null=True, blank=True)
    lieu_naissance = models.CharField(max_length=255, null=True, blank=True)

    bank = models.CharField(max_length=255, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name="Employe"
        verbose_name_plural="Employes"

    def __str__(self):
        return f"{self.nom} {self.prenom}"


class Conges(models.Model):
    tenant = models.ForeignKey(Institut, on_delete=models.CASCADE, null=True, blank=True)
    employee = models.ForeignKey(Employees, on_delete=models.CASCADE, null=True, blank=True)

    date_debut = models.DateField()
    date_fin = models.DateField()

    motif = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name="Conge"
        verbose_name_plural="Conges"

    def __str__(self):
        return f"{self.employee.nom} {self.employee.prenom}"
    
class Paie(models.Model):
    tenant = models.ForeignKey(Institut, on_delete=models.CASCADE, null=True, blank=True)
    employee = models.ForeignKey(Employees, on_delete=models.CASCADE, null=True, blank=True)

    salaire = models.DecimalField(max_digits=200, decimal_places=2, null=True, blank=True)
    date_paie = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name="Paie"
        verbose_name_plural="Paies"

    def __str__(self):
        return f"{self.employee.nom} {self.employee.prenom}"