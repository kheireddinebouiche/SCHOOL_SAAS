from django.db import models
from django.contrib.auth.models import User
from institut_app.models import Entreprise
from t_rh.models import *


class Partenaires(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    nom = models.CharField(max_length=255, null=True, blank=True)
    code = models.CharField(max_length=255, null=True, blank=True, unique=True)
    adresse = models.CharField(max_length=255, null=True, blank=True)
    telephone = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    site_web = models.URLField(null=True, blank=True)
    type_partenaire = models.CharField(max_length=100, null=True, blank=True, choices=[('national', 'Partenaire National'),('etranger','Partenaire Etranger')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="updated_by_partenaire")

    class Meta:
        verbose_name="Partenaire"
        verbose_name_plural="Partenaires"

    def __str__(self):
        return self.nom

class Formation(models.Model):
    code = models.CharField(max_length=100, null=True, blank=True, unique=True)
    nom = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    duree = models.PositiveIntegerField()
    date_creation = models.DateTimeField(auto_now_add=True)
    entite_legal = models.ForeignKey(Entreprise, on_delete=models.SET_NULL, null=True, blank=True)
    partenaire = models.ForeignKey(Partenaires, on_delete=models.SET_NULL, null=True, blank=True, to_field="code")
    type_formation = models.CharField(choices=[('etrangere', 'Formation étrangere'), ('national', 'Formation Etatique')], max_length=100, null=True, blank=True, default='national')
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    frais_inscription = models.DecimalField(max_digits=10, null=True, blank=True, decimal_places=2)
    frais_assurance = models.DecimalField(max_digits=10, null=True, blank=True, decimal_places=2)
    updated = models.BooleanField(default=False)

    class Meta:
        verbose_name="Formation"
        verbose_name_plural="Formations"

    def __str__(self):
        return self.nom

class DossierInscription(models.Model):
    formation = models.ForeignKey(Formation, on_delete=models.DO_NOTHING, null=True, blank=True)
    label = models.CharField(max_length=100, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.label

class Specialites(models.Model):
    code = models.CharField(max_length=100, null=True, blank=True, unique =True)
    label = models.CharField(max_length=100, null=True, blank=True)
    prix = models.DecimalField(decimal_places=2, max_digits=100, null=True, blank=True)
    duree = models.CharField(max_length=300, null=True, blank=True)
    nb_semestre = models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')], null=True, blank=True, max_length=1)

    formation = models.ForeignKey(Formation, on_delete=models.CASCADE, null=True, blank=True,to_field="code", related_name="formation_specilite")

    nb_tranche = models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')], null=True, blank=True, max_length=1)
    responsable = models.ForeignKey(Employees, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True, related_name="specialite_updated_by")
    version = models.CharField(max_length=100, null=True, blank=True)
    condition_access = models.TextField(max_length=1000, null=True, blank=True)
    dossier_inscription = models.TextField(max_length=1000, null=True, blank=True)

    etat = models.CharField(max_length=10, null=True, blank=True, choices=[('last','A jour'),('updated','Mis à jour')], default='last')

    class Meta:
        verbose_name="Spécialité"
        verbose_name_plural="Spécialités"

    def __str__(self):
        return f"{self.code} - {self.label}"
    
class Modules(models.Model):
   
    specialite = models.ForeignKey(Specialites, on_delete=models.CASCADE, null=True, blank=True, to_field="code")
    code = models.CharField(max_length=100, null=True, blank=True, unique=True)
    label = models.CharField(max_length=100, null=True, blank=True)
    
    duree = models.IntegerField(null=True, blank=True)

    coef = models.IntegerField(null=True, blank=True)
    n_elimate = models.IntegerField(null=True, blank=True)

    systeme_eval = models.CharField(max_length=100, null=True, blank=True)

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
    
class PlansCadre(models.Model):
    module = models.ForeignKey(Modules, on_delete=models.CASCADE, null=True, blank=True)
    titre = models.CharField(max_length=255,null=True, blank=True)
    objectifs = models.TextField(null=True, blank=True)
    competences_visees = models.TextField(null=True, blank=True)
    prerequis = models.TextField(blank=True, null=True)
    contenus = models.TextField(null=True, blank=True)
    volume_cours = models.PositiveIntegerField(help_text="Heures de cours magistral", default=0)
    volume_td = models.PositiveIntegerField(help_text="Heures de travaux dirigés", default=0)
    volume_tp = models.PositiveIntegerField(help_text="Heures de travaux pratiques", default=0)
    methodes_pedagogiques = models.TextField(null=True, blank=True)
    modalites_evaluation = models.TextField(null=True, blank=True)
    bibliographie = models.TextField(blank=True, null=True)
    responsable = models.CharField(max_length=255, null=True, blank=True)       
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        verbose_name="Plan cadre"
        verbose_name_plural = "Plans cadre"
    
    def __str__(self):
        return f"{self.module.label} {self.module.code}"

class ProgrammePlanCadre(models.Model):
    plan_cadre = models.ForeignKey(PlansCadre, on_delete=models.CASCADE, null=True, blank=True)

    element_competence = models.TextField(null=True, blank=True)
    criters_performance = models.TextField(null=True, blank=True)
    contenu_pedagogique = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.plan_cadre.module.label} {self.plan_cadre.module.code} - {self.element_competence}"

class PlansCours(models.Model):
    pass

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
    
class ProgrammeFormation(models.Model):
    module = models.ForeignKey(Modules, on_delete=models.CASCADE, null=True, blank=True,to_field="code")
    specialite = models.ForeignKey(Specialites, on_delete=models.CASCADE, null=True, blank=True, to_field="code")
    semestre = models.CharField(max_length=10, null=True, blank=True)

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

    etat = models.CharField(max_length=10, null=True, blank=True, choices=[('active','Active'),('inactive','Inactive')], default='inactive')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name="Promo"
        verbose_name_plural="Promos"

    def __str__(self):
        return f"{self.label} - {self.session}"