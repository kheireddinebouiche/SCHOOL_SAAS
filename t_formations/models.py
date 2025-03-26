from django.db import models
from django.contrib.auth.models import User
from institut_app.models import Entreprise
from t_rh.models import *


class Formation(models.Model):
    nom = models.CharField(max_length=255)

    description = models.TextField(null=True, blank=True)

    duree = models.PositiveIntegerField()

    date_creation = models.DateTimeField(auto_now_add=True)

    entite_legal = models.ForeignKey(Entreprise, on_delete=models.SET_NULL, null=True, blank=True)

    partenaire = models.ForeignKey('Partenaires', on_delete=models.SET_NULL, null=True, blank=True)

    type_formation = models.CharField(choices=[('etrangere', 'Formation étrangere'), ('national', 'Formation Etatique')], max_length=100, null=True, blank=True, default='national')
    
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    frais_inscription = models.DecimalField(max_digits=10, null=True, blank=True, decimal_places=2)
    frais_assurance = models.DecimalField(max_digits=10, null=True, blank=True, decimal_places=2)

    def __str__(self):
        return self.nom
    
class Specialites(models.Model):

    code = models.CharField(max_length=100, null=True, blank=True, unique=True)
    label = models.CharField(max_length=100, null=True, blank=True)

    prix = models.DecimalField(decimal_places=2, max_digits=100, null=True, blank=True)

    duree = models.CharField(max_length=300, null=True, blank=True)

    nb_semestre = models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')], null=True, blank=True, max_length=1)

    formation = models.ForeignKey(Formation, on_delete=models.CASCADE, null=True, blank=True)

    nb_tranche = models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')], null=True, blank=True, max_length=1)

    responsable = models.ForeignKey(Employees, on_delete=models.SET_NULL, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)

    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True, related_name="specialite_updated_by")

    version = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name="Spécialité"
        verbose_name_plural="Spécialités"

    def __str__(self):
        return self.label
    
class Modules(models.Model):
    specialite = models.ForeignKey(Specialites, on_delete=models.CASCADE, null=True, blank=True)
    code = models.CharField(max_length=100, null=True, blank=True)
    label = models.CharField(max_length=100, null=True, blank=True)
    
    duree = models.IntegerField(null=True, blank=True)

    coef = models.IntegerField(null=True, blank=True)
    n_elimate = models.IntegerField(null=True, blank=True)

    is_archived = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(User, on_delete = models.SET_NULL, blank=True, null=True, related_name="module_created_by")
    updated_by = models.ForeignKey(User, on_delete = models.SET_NULL, blank=True, null=True, related_name="module_updated_by")
    
    class Meta:
        verbose_name="Module"
        verbose_name_plural="Modules"

    def __str__(self):
        return self.label
    
class FraisInscription(models.Model):
    specialite = models.ForeignKey(Specialites, on_delete=models.CASCADE, null=True, blank=True)
    label = models.CharField(max_length=255, null=True, blank=True)
    montant = models.DecimalField(max_digits=200, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name="Frais d'inscription"
        verbose_name_plural="Frais d'inscription"

    def __str__(self):
        return self.label
    
class Partenaires(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    nom = models.CharField(max_length=255, null=True, blank=True)
    code = models.CharField(max_length=255, null=True, blank=True)
    adresse = models.CharField(max_length=255, null=True, blank=True)
    telephone = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    site_web = models.URLField(null=True, blank=True)
    type_partenaire = models.CharField(max_length=100, null=True, blank=True, choices=[('national', 'National'),('etranger','Etranger')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="updated_by_partenaire")

    class Meta:
        verbose_name="Partenaire"
        verbose_name_plural="Partenaires"

    def __str__(self):
        return self.nom

class ProgrammeFormation(models.Model):
    module = models.ForeignKey(Modules, on_delete=models.CASCADE, null=True, blank=True)
    specialite = models.ForeignKey(Specialites, on_delete=models.CASCADE, null=True, blank=True)
    semestre = models.CharField(choices=[('1','1'),('2','2'),('3','3'),('4','4')], max_length=1, null=True, blank=True)


    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        verbose_name="Repartition du module"
        verbose_name_plural = "Repartition des modules"
        unique_together = ('module','specialite','semestre')

    def __str__(self):
        return f"{self.module.label} - {self.semestre}"
    
class Promos(models.Model):
    
    label = models.CharField(max_length=255, null=True, blank=True)
    session = models.CharField(max_length=255, null=True, blank=True, choices=[('octobre', 'Octobre'), ('mars', 'Mars')])

    etat = models.CharField(max_length=10, null=True, blank=True, choices=[('active','Active'),('inactive','Inactive')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name="Promo"
        verbose_name_plural="Promos"

    def __str__(self):
        return self.label