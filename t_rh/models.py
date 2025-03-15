from django.db import models
from app.models import *
from django.contrib.auth.models import User
from institut_app.models import *


class Employees(models.Model):
    tenant = models.ForeignKey(Institut, on_delete=models.CASCADE, null=True, blank=True)
    nom = models.CharField(max_length=255, null=True, blank=True)
    prenom = models.CharField(max_length=255, null=True, blank=True)
    civilite = models.CharField(max_length=100, null=True, blank=True, choices=[('mr','Mr.'),('mme','Mme'),('mlle','Mlle')])
    email = models.EmailField(null=True, blank=True)
    telephone = models.CharField(max_length=15, null=True, blank=True)

    adresse = models.TextField(null=True, blank=True)

    cin = models.CharField(max_length=255, null=True, blank=True)
    nin = models.CharField(max_length=255, null=True, blank=True)
    secu = models.CharField(max_length=255, null=True, blank=True) 

    situation_familiale = models.CharField(max_length=255, null=True, blank=True, choices=[('C', 'Célibataire'), ('M', 'Marié(e)'), ('D', 'Divorcé(e)'), ('V', 'Veuf(ve)')])
    sexe = models.CharField(max_length=1, null=True, blank=True, choices=[('M', 'Masculin'), ('F', 'Feminin')])
    date_naissance = models.DateField(null=True, blank=True)
    lieu_naissance = models.CharField(max_length=255, null=True, blank=True)

    bank = models.CharField(max_length=255, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    has_contract = models.BooleanField(default=False)

    work_in = models.ForeignKey(Entreprise, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name="Employe"
        verbose_name_plural="Employes"

    def __str__(self):
        return f"{self.nom} {self.prenom}"

class Absences(models.Model):
    pass

class Services(models.Model):
    label = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name="Service"
        verbose_name_plural="Services"

    def __str__(self):
        return self.label

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

class LigneFicheDePaie(models.Model):
    pass

class TemplateFichePaie(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    label = models.CharField(max_length=100, null=True, blank=True)
    mode = models.CharField(max_length=100, null=True, blank=True, choices=[('vacataire','Enseignant vacataire'),('employe','Employe(e)')])

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name="Temple fiche de paie"
        verbose_name_plural = "Templates fiche de paie"

    def __str__(self):
        return self.label

class Contrats(models.Model):
    employee = models.ForeignKey(Employees, on_delete=models.CASCADE, null=True, blank=True, related_name="contrats")
    type_contrat = models.CharField(max_length=255, null=True, blank=True, choices=[('cdi', 'CDI'), ('cdd', 'CDD'), ('stage', 'Stage'), ('interim', 'Interim')])

    date_debut = models.DateField()
    date_fin = models.DateField()

    poste = models.CharField(max_length=255, null=True, blank=True, choices=[('emp','Employe(e)'), ('dir', 'Directeur(trice)'), ('per', 'Enseignant permanant'), ('vac', 'Enseignant vacataire')])
    service = models.ForeignKey('Services', on_delete=models.SET_NULL, null=True, blank=True)

    salaire = models.DecimalField(max_digits=200, decimal_places=2, null=True, blank=True)
    date_embauche = models.DateField(null=True, blank=True)
    date_depart = models.DateField(null=True, blank=True)

    motif = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name="Contrat"
        verbose_name_plural="Contrats"

    def __str__(self):
        return f"{self.employee.nom} {self.employee.prenom}"
    
class ArticlesContrat(models.Model):
    titre = models.CharField(max_length=255, blank=True, null=True)
    contenu = models.TextField()
    type_contrat = models.CharField(
        max_length=20,
        choices=[
            ('CDD', 'Contrat à Durée Déterminée'),
            ('CDI', 'Contrat à Durée Indéterminée'),
            ('Stage', 'Stage'),
            ('Vacation', 'Vacation'),
            ('Tous', 'Applicable à tous')
        ],blank=True, null=True
    )

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.titre