from django.db import models
from app.models import *
from django.contrib.auth.models import User
from institut_app.models import *


class Employees(models.Model):
    
    nom = models.CharField(max_length=255, null=True, blank=True)
    prenom = models.CharField(max_length=255, null=True, blank=True)
    civilite = models.CharField(max_length=100, null=True, blank=True, choices=[('mr','Mr.'),('mme','Mme'),('mlle','Mlle')])
    email = models.EmailField(null=True, blank=True)
    telephone = models.CharField(max_length=15, null=True, blank=True)

    adresse = models.TextField(null=True, blank=True)

    prenom_pere = models.CharField(max_length=100, null=True, blank=True)
    nom_mere = models.CharField(max_length=100, null=True, blank=True)
    prenom_mere = models.CharField(max_length=100, null=True, blank=True)

    cin = models.CharField(max_length=255, null=True, blank=True)
    nin = models.CharField(max_length=255, null=True, blank=True)
    secu = models.CharField(max_length=255, null=True, blank=True) 

    situation_familiale = models.CharField(max_length=255, null=True, blank=True, choices=[('C', 'Célibataire'), ('M', 'Marié(e)'), ('D', 'Divorcé(e)'), ('V', 'Veuf(ve)')])
    sexe = models.CharField(max_length=1, null=True, blank=True, choices=[('M', 'Masculin'), ('F', 'Feminin')])

    groupe_sanguin = models.CharField(max_length=5, null=True, blank=True, choices=[
        ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')
    ])
    
    date_naissance = models.DateField(null=True, blank=True)
    lieu_naissance = models.CharField(max_length=255, null=True, blank=True)

    bank = models.CharField(max_length=255, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    has_contract = models.BooleanField(default=False)
    etat = models.CharField(max_length=100, null=True, blank=True, choices=[('en cours', "En cours d'activité"),('demission',"Démissionnaire")])

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

class Posts(models.Model):
    label = models.CharField(max_length=100, null=True, blank=True)
    service = models.ForeignKey(Services, null=True, blank=True, on_delete=models.SET_NULL)
    description = models.CharField(max_length=1000, null=True, blank=True)

    class Meta:
        verbose_name="Poste"
        verbose_name_plural="Posts"

    def __str__(self):
        return self.label

class TachesPoste(models.Model):
    poste = models.ForeignKey(Posts, on_delete=models.CASCADE, null=True)
    label = models.CharField(max_length=100, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta: 
        verbose_name="Tache"
        verbose_name_plural = "Taches"
    
    def __str__(self):
        return self.label

class Conges(models.Model):
    
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

class CategoriesContrat(models.Model):
    
    label = models.CharField(max_length=100, null=True)
    entite_legal = models.ForeignKey(Entreprise, on_delete=models.SET_NULL, null=True)
    description = models.CharField(max_length=100, null=True, blank=True)

    etat = models.CharField(max_length=100, null=True, choices=[('active', "Activé"),('disabled','Désactivé')], default='active')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name="Catégorie de contrat"
        verbose_name_plural="Catégories de contrat"
    
    def __str__(self):
        return self.label

class TypesContrat(models.Model):
    label = models.CharField(max_length=255, null=True)
    categorie = models.ForeignKey(CategoriesContrat, null=True, on_delete=models.SET_NULL)
    description = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name="Type de contrat"
        verbose_name_plural="Types de contrat"

    def __str__(self):
        return self.label

class Contrats(models.Model):
    employee = models.ForeignKey(Employees, on_delete=models.CASCADE, null=True, blank=True, related_name="contrats")
    type_contrat = models.ForeignKey(TypesContrat, on_delete=models.CASCADE, null=True, blank=True, related_name="contrats")

    date_fin = models.DateField(null=True)

    poste = models.ForeignKey(Posts, null=True, on_delete=models.SET_NULL)
    service = models.ForeignKey('Services', on_delete=models.SET_NULL, null=True, blank=True)

    salaire_base = models.DecimalField(max_digits=200, decimal_places=2, null=True, blank=True)
    date_embauche = models.DateField(null=True, blank=True)
    date_depart = models.DateField(null=True, blank=True)
    duree = models.CharField(max_length=100, null=True, blank=True)

    motif = models.TextField(null=True, blank=True)

    has_essai = models.BooleanField(null=True, blank=True)
    periode_essai = models.CharField(max_length=100, null=True, blank=True)
    mode_essei = models.CharField(max_length=100, null=True, blank=True, choices=[('m','Mois'),('a','Années')], default='m')
    observations = models.CharField(max_length=1000, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name="Contrat"
        verbose_name_plural="Contrats"

    def __str__(self):
        return f"{self.employee.nom} {self.employee.prenom}"
    
class ArticlesContratStandard(models.Model):
    titre = models.CharField(max_length=255, blank=True, null=True)
    contenu = models.TextField(null=True)
    type_contrat = models.ForeignKey(TypesContrat, on_delete=models.CASCADE, null=True, blank=True, related_name="articles")

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.titre
    
class ArticleContratSpecial(models.Model):
    contrat = models.ForeignKey(Contrats, on_delete=models.CASCADE, null=True, blank=True, related_name="articles_special")

    label = models.CharField(max_length=255, blank=True)
    contenu = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name="Article de contrat special"
        verbose_name_plural="Articles de contrat special"

    def __str__(self):
        return self.label