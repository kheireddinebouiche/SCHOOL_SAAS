from django.db import models
from django.contrib.auth.models import User
from institut_app.models import Entreprise
from t_rh.models import *
from t_crm.tenant_path import *
from pdf_editor.models import *
from django.db.models import Max

class Partenaires(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    logo = models.ImageField(upload_to=tenant_directory_path_for_logos, null=True, blank=True)
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

    etat = models.CharField(max_length=10, null=True, blank=True, choices=[('active','Active'),('inactive','Inactive')], default='active')
    observation = models.TextField(null=True, blank=True)

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
    type_formation = models.CharField(choices=[('etrangere', 'Formation étrangère'), ('national', 'Formation Etatique')], max_length=100, null=True, blank=True, default='national')
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    frais_inscription = models.DecimalField(max_digits=10, null=True, blank=True, decimal_places=2)
    updated = models.BooleanField(default=False)
    qualification = models.CharField(max_length=10, null=True, blank=True)
    prix_formation = models.DecimalField(max_digits=10, null=True, blank=True, decimal_places=2)

    documents = models.ManyToManyField(DocumentTemplate)

    class Meta:
        verbose_name="Formation"
        verbose_name_plural="Formations"

    def __str__(self):
        return self.nom

class DossierInscription(models.Model):
    formation = models.ForeignKey(Formation, on_delete=models.DO_NOTHING, null=True, blank=True)
    label = models.CharField(max_length=100, null=True, blank=True)
    is_required = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.label

class Specialites(models.Model):
    code = models.CharField(max_length=100, null=True, blank=True, unique =True)
    label = models.CharField(max_length=100, null=True, blank=True)
    prix = models.DecimalField(decimal_places=2, max_digits=100, null=True, blank=True)
    prix_double_diplomation = models.DecimalField(decimal_places=2, max_digits=100, null=True, blank=True)
    duree = models.CharField(max_length=300, null=True, blank=True)
    nb_semestre = models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')], null=True, blank=True, max_length=1)
    branche = models.CharField(max_length=100, null=True, blank=True)
    abr = models.CharField(max_length=100, null=True, blank=True)
    branche = models.CharField(max_length=2555, null=True, blank=True)
    formation = models.ForeignKey(Formation, on_delete=models.CASCADE, null=True, blank=True,to_field="code", related_name="formation_specilite")

    nb_tranche = models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')], null=True, blank=True, max_length=1)
    responsable = models.ForeignKey(Employees, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True, related_name="specialite_updated_by")
    version = models.CharField(max_length=100, null=True, blank=True)
    condition_access = models.TextField(max_length=1000, null=True, blank=True)

    etat = models.CharField(max_length=10, null=True, blank=True, choices=[('last','À jour'),('updated','Mis à jour')], default='last')

    class Meta:
        verbose_name="Spécialité"
        verbose_name_plural="Spécialités"

    def __str__(self):
        return self.label
    
class DoubleDiplomation(models.Model):
    label = models.CharField(max_length=100, null=True, blank=True)
    specialite1 = models.ForeignKey(Specialites, related_name="double_spec1", on_delete = models.DO_NOTHING, null=True, blank=True)
    specialite2 = models.ForeignKey(Specialites, related_name="double_spec2", on_delete = models.DO_NOTHING, null=True, blank=True)
    frais_inscription = models.DecimalField(max_digits=100, decimal_places=2 ,null=True, blank=True)

    prix_spec1 = models.DecimalField(max_digits=100, decimal_places=2, null=True, blank=True)
    prix_spec2 = models.DecimalField(max_digits=100, decimal_places=2, null=True, blank=True)

    prix = models.DecimalField(decimal_places=2, max_digits=100, null=True, blank=True)

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.label
    
class Modules(models.Model):
   
    specialite = models.ForeignKey(Specialites, on_delete=models.CASCADE, null=True, blank=True)
    code = models.CharField(max_length=100, null=True, blank=True, unique=True)
    code_interne = models.CharField(max_length=100, null=True, blank=True)
    label = models.CharField(max_length=100, null=True, blank=True)
    
    duree = models.IntegerField(null=True, blank=True)

    coef = models.IntegerField(null=True, blank=True)
    n_elimate = models.IntegerField(null=True, blank=True)

    systeme_eval = models.CharField(max_length=100, null=True, blank=True)

    is_archived = models.BooleanField(default=False)
    est_valider = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(User, on_delete = models.SET_NULL, blank=True, null=True, related_name="module_created_by")
    updated_by = models.ForeignKey(User, on_delete = models.SET_NULL, blank=True, null=True, related_name="module_updated_by")
    

    class Meta:
        verbose_name="Module"
        verbose_name_plural="Modules"
        unique_together = ('code_interne', 'specialite')

    def __str__(self):
        return self.code
    
    # 🔹 Génération du code
    def generate_code(self):
        if not self.specialite:
            return None

        # Numéro de la spécialité
        specialite_index = self.specialite.id

        # Dernier numéro utilisé pour cette spécialité
        last_code = (
            Modules.objects
            .filter(specialite=self.specialite, code__isnull=False)
            .aggregate(max_code=Max('code'))
        )['max_code']

        if last_code:
            last_number = int(last_code.split('-')[-1])
            next_number = last_number + 1
        else:
            next_number = 1

        return f"M-{specialite_index}-{str(next_number).zfill(3)}"

    # 🔹 Override save()
    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_code()
        super().save(*args, **kwargs)

class CorrepondanceModule(models.Model):
    label = models.CharField(max_length=100, null=True, blank=True)
    formation = models.ForeignKey(DoubleDiplomation, on_delete=models.CASCADE, null=True, blank=True)
    modules = models.ManyToManyField(Modules)

    created_at = models.DateField(auto_now_add = True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.label

class Formateurs(models.Model):
    nom = models.CharField(max_length=100, null=True, blank=True)
    prenom = models.CharField(max_length=100, null=True, blank=True)
    telephone = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    diplome = models.CharField(max_length=100, null=True, blank=True)
    dispo = models.JSONField(default=dict, blank=True, null=True)


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nom} - {self.prenom}"
    
class EnseignantModule(models.Model):
    module = models.ForeignKey(Modules, on_delete=models.CASCADE, null=True, blank=True, related_name="affect_module")
    formateur = models.ForeignKey(Formateurs, on_delete=models.CASCADE, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.module.label}"
        
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
    module = models.ForeignKey(Modules, on_delete=models.CASCADE, null=True, blank=True)
    specialite = models.ForeignKey(Specialites, on_delete=models.CASCADE, null=True, blank=True)
    semestre = models.CharField(max_length=10, null=True, blank=True)

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        verbose_name="Répartition du module"
        verbose_name_plural = "Répartition des modules"
        unique_together = ('module', 'semestre')

    def __str__(self):
        return f"{self.module.label} - {self.semestre}"
    
class Promos(models.Model):
    
    label = models.CharField(max_length=255, null=True, blank=True)
    code = models.CharField(max_length = 255, null=True, blank=True)
    begin_year = models.CharField(null=True, blank=True)
    end_year = models.CharField(null=True, blank=True)
    session = models.CharField(max_length=255, null=True, blank=True, choices=[('octobre', 'Octobre'), ('mars', 'Mars')])
    annee_academique = models.CharField(max_length=255, null=True, blank=True)

    date_debut = models.DateField(null=True)
    date_fin = models.DateField(null=True)

    etat = models.CharField(max_length=10, null=True, blank=True, choices=[('active','Active'),('inactive','Inactive')], default='inactive')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    prix_rachat_credit =models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    penalite_retard = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    entite = models.ForeignKey(Entreprise, null=True, blank=True, on_delete=models.DO_NOTHING)

    is_archived = models.BooleanField(default=False)

    class Meta:
        verbose_name="Promo"
        verbose_name_plural="Promos"

    def __str__(self):
        return f"{self.label} - {self.session}"