from django.db import models
from django.contrib.auth.models import User, Group
from app.models import Institut
from django_countries.fields import CountryField
from t_crm.tenant_path import *

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    adresse = models.CharField(max_length=100, null=True, blank=True)
    role = models.CharField(max_length=100, null=True, blank=True, choices=[('admin', 'Admin'), ('user', 'User'),('tresorier', 'Trésorier'),('rh', 'Ressources Humaines'),('crm', 'Chargé(e) clientèle')])
    image = models.ImageField(upload_to='profile_images', null=True, blank=True, default='profile_images/default1.png')
    class Meta:
        verbose_name="Profile"
        verbose_name_plural="Profiles"
    
    def __str__(self):
        return self.user.username
    
class CustomGroupe(Group):
    description = models.CharField(max_length=100, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name="Groupe"
        verbose_name_plural = "Groupes"
    
    def __str__(self):
        return self.name

class Roles(models.Model):
    label = models.CharField(max_length=100, null=True, blank=True)

    can_edit = models.BooleanField(default=True)
    can_delete = models.BooleanField(default=True)
    can_add = models.BooleanField(default=True)
    can_validate = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name="Role"
        verbose_name_plural="Roles"

    def __str__(self):
        return self.label

class Entreprise(models.Model):
    tenant = models.ForeignKey(Institut, on_delete=models.CASCADE, null=True, blank=True)
    designation = models.CharField(max_length=255, null=True, blank=True)
    logo = models.ImageField(upload_to=tenant_directory_path_for_logos, null=True, blank=True)

    rc = models.CharField(max_length=255, null=True, blank=True)
    nif = models.CharField(max_length=255, null=True, blank=True)
    art = models.CharField(max_length=255, blank=True, null=True)
    nis = models.CharField(max_length=255, null=True, blank=True)

    adresse = models.CharField(max_length=255, null=True, blank=True)
    telephone = models.CharField(max_length=255, null=True, blank=True)
    wilaya = models.CharField(max_length=255, null=True, blank=True)
    pays = CountryField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    site_web = models.URLField(null=True, blank=True)
    entete = models.TextField(null=True, blank=True)


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name="Entreprise"
        verbose_name_plural = "Entreprises"
    
    def __str__(self):
        return self.designation

class BankAccount(models.Model):
    tenant = models.ForeignKey(Institut, on_delete=models.CASCADE, null=True, blank=True)
    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE, null=True, blank=True)
    label = models.CharField(max_length=255, null=True, blank=True)
    num = models.CharField(max_length=255, null=True, blank=True)
    amount = models.DecimalField(max_digits=200, decimal_places=2, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name="Label"
        verbose_name_plural="Labels"

    def __str__(self):
        return self.label

class Settings(models.Model):
    tenant = models.ForeignKey(Institut, on_delete=models.CASCADE, null=True, blank=True)
    
    class Meta:
        verbose_name="Paramètre"
        verbose_name_plural="Paramètres"

    def __str__(self):
        return self.tenant.nom
    
class SalleClasse(models.Model):
    label = models.CharField(max_length=100, null=True)
    etage = models.CharField(max_length=100, null=True, blank=True)
    nb_place = models.IntegerField(null=True, blank=True)
    surface = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name="Salle de classe"
        verbose_name_plural="Salles de classe"

    def __str__(self):
        return f"{self.label} - {self.etage}"

class ConfigurationDesDocument(models.Model):
    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE, null=True, blank=True)
    prefix_devis = models.CharField(max_length=50, null=True, blank=True, help_text="Préfixe pour les devis")
    prefix_facture = models.CharField(max_length=50, null=True, blank=True, help_text="Préfixe pour les factures")

    class Meta:
        verbose_name = "Configuration des documents"
        verbose_name_plural = "Configurations des documents"

    def __str__(self):
        return f"Configuration des documents pour {self.entreprise.designation}" if self.entreprise else "Configuration des documents sans entreprise"
