from django.db import models
from django.contrib.auth.models import User, Group
from app.models import Institut
from django_countries.fields import CountryField
from t_crm.tenant_path import *
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

class UserSession(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="session_info")
    last_session_key = models.CharField(max_length=40, null=True, blank=True)

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
   
    designation = models.CharField(max_length=255, null=True, blank=True)
    logo = models.ImageField(upload_to=tenant_directory_path_for_logos, null=True, blank=True)
    entete_logo = models.ImageField(upload_to=tenant_directory_path_for_logos, null=True, blank=True)
    pied_page_logo = models.ImageField(upload_to=tenant_directory_path_for_logos, null=True, blank=True)
    rc = models.CharField(max_length=255, null=True, blank=True)
    nif = models.CharField(max_length=255, null=True, blank=True)
    art = models.CharField(max_length=255, blank=True, null=True)
    nis = models.CharField(max_length=255, null=True, blank=True)

    adresse = models.CharField(max_length=255, null=True, blank=True)
    telephone = models.CharField(max_length=255, null=True, blank=True)
    ville = models.CharField(max_length = 222 ,null=True, blank=True)
    wilaya = models.CharField(max_length=255, null=True, blank=True)
    pays = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    site_web = models.URLField(null=True, blank=True)
    entete = models.TextField(null=True, blank=True)
    code_postal = models.CharField(max_length=100, null=True, blank=True)
    observations = models.TextField(null=True, blank=True)
    representant = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    code_wilaya = models.CharField(max_length=100, null=True, blank=True)
    numero = models.CharField(max_length=100, null=True, blank=True)

    entite_afficher = models.CharField(max_length=100, null=True, blank=True, help_text="Abreviation a afficher sur les rapport ex: INSIM")

    class Meta:
        verbose_name="Entreprise"
        verbose_name_plural = "Entreprises"
    
    def __str__(self):
        return self.designation

class BankAccount(models.Model):
   
    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE, null=True, blank=True, related_name="comptes_entreprise")
    bank_name = models.CharField(max_length=255, null=True, blank=True)
    bank_code = models.CharField(max_length=100, null=True, blank=True)
    bank_iban  = models.CharField(max_length=1000, null=True, blank=True)
    bank_currency  = models.CharField(max_length=1000, null=True, blank=True, choices=[('eur','Euro'),('dzd','Dinars'),('usd','USD')])
    bank_observations = models.CharField(max_length=1000, null=True, blank=True)

    is_archived = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name="Label"
        verbose_name_plural="Labels"

    def __str__(self):
        return self.bank_code

class Settings(models.Model):
    
    
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

class Fournisseur(models.Model):
    designation = models.CharField(max_length=100, null=True, blank=True)
    telephone = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    site_web = models.CharField(max_length=100, null=True, blank=True)
    code = models.CharField(max_length=100, null=True, blank=True)
    adresse = models.CharField(max_length=100, null=True, blank=True)
    commune = models.CharField(max_length=100, null=True, blank=True)
    wilaya = models.CharField(max_length=100, null=True, blank=True)
    pays = models.CharField(max_length=100, null=True, blank=True)

    rc = models.CharField(max_length=100, null=True, blank=True)
    nif = models.CharField(max_length=100, null=True, blank=True)
    art = models.CharField(max_length=100, null=True, blank=True)
    nis = models.CharField(max_length=100, null=True, blank=True)

    banque = models.CharField(max_length=100, null=True, blank=True)
    num_compte = models.CharField(max_length=100, null=True, blank=True)
    code_banque = models.CharField(max_length=100, null=True, blank=True)
    observation = models.TextField(null=True, blank=True)

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    
    def __str__(self):
        return self.designation

class Module(models.Model):
    MODULES = [
        ('crm',_('CRM')),
        ('ped',_('Pédagogie')),
        ('eva',_('Evaluation')),
        ('con',_('Conseil')),
        ('adm',_('Administration')),
    ]

    name = models.CharField(max_length=50, null=True, blank=True, choices=MODULES, unique=True, verbose_name=_("Module"))
    description = models.TextField(max_length=50, blank=True, verbose_name=_('Description'))
    is_active = models.BooleanField(default=True, verbose_name=_('Actif'))
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)


    class Meta:
        verbose_name=_('Module')
        verbose_name_plural = _('Modules')
        ordering = ['name']

    def __str__(self):
        return self.get_name_display()
    
class Role(models.Model):
    ROLE_LEVEL = [
        (1, _('Utilisateur')),
        (2, _('Superviseur')),
        (3, _('Manager')),
        (4, _('Administrateur')),
    ]

    name = models.CharField(max_length=50, unique=True, verbose_name=_('Nom du Rôle'))

    level = models.IntegerField(choices=ROLE_LEVEL, verbose_name=_('Niveau'))
    description = models.TextField(blank=True, verbose_name=_('Description'))
    is_active = models.BooleanField(default=True, verbose_name=_('Actif'))
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        verbose_name=_('Role')
        verbose_name_plural=_('Roles')
        ordering = ['-level', 'name']


    def __str__(self):
        return self.name

class ModulePermission(models.Model):
    PERMISSION_TYPE = [
        ('view', _('Visualiser')),
        ('add', _('Ajouter')),
        ('change', _('Modifier')),
        ('delete', _('Supprimer')),
        ('export', _('Exporter')),
        ('approuv', _('Approuver')),
    ]

    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name="permissions", verbose_name=_('Module'))
    permission_type = models.CharField(max_length=20, choices=PERMISSION_TYPE, verbose_name=_('Type de permission'))
    description = models.TextField(blank=True, verbose_name=_('Description'))

    class Meta:
        verbose_name=_('Permission de Module')
        verbose_name_plural= _('Permissions de module')
        unique_together = ('module','permission_type')
        ordering = ['module','permission_type']

    def __str__(self):
        return f"{self.module.get_name_display()} - {self.get_permission_type_display()}"
    
class RolePermission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='permissions', verbose_name=_('Role'))
    module_permission = models.ForeignKey(ModulePermission, on_delete=models.CASCADE, related_name='roles', verbose_name=_('Permission'))
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        verbose_name=_('Permission de Role')
        verbose_name_plural = _('Permissions de Role')
        unique_together = ('role', 'module_permission')
        ordering = ['role','module_permission__module']


    def __str__(self):
        return f"{self.role.name} - {self.module_permission}"
    
class UserModuleRole(models.Model):

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='module_roles', verbose_name=_('Utilisateur'))
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name="user_roles", verbose_name=_('Module'))
    role = models.ForeignKey(Role, on_delete=models.PROTECT, verbose_name=_('Role'))
    assigned_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, related_name="assigned_roles", verbose_name=_('Assigné par'))
    assigned_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        verbose_name=_('Role Utilisateur-Module')
        verbose_name_plural = _('Roles Utilisteur-Module')
        unique_together = ('user','module')
        ordering = ['user','module','-role__level']
        indexes = [
            models.Index(fields=['user','module']),
            models.Index(fields=['module','role']),
        ]

    def __str__(self):
        return f"{self.user} - {self.module.get_name_display()} - {self.role.name}"
    
    def has_permission(self, permission_type):
        return self.role.permissions.filter(
            module_permission__module = self.module,
            module_permission__permission_type = permission_type
        ).exists()