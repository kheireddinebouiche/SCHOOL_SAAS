from django_tenants.models import TenantMixin,DomainMixin
from django.db import models
from django.utils.translation import gettext_lazy as _


class Institut(TenantMixin):
    nom = models.CharField(max_length=255, unique=True)
    adresse = models.TextField(null=True, blank=True)
    telephone = models.CharField(max_length=15, null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    tenant_type = models.CharField(max_length=255, null=True, blank=True, choices=[('associe','Associe'),('master','Compte maitre'),('second','Compte standard')])
    is_visible = models.BooleanField(default=True, verbose_name=_("Visible dans la sélection"))
    is_active = models.BooleanField(default=True, verbose_name=_("Compte actif"))
    crm_notifications_enabled = models.BooleanField(default=True, verbose_name=_("Notifications CRM actives"))
    max_upload_size = models.PositiveIntegerField(null=True, blank=True, verbose_name=_("Taille max upload (KB)"), help_text=_("Laissez vide pour utiliser la limite globale du SaaS"))
    
    force_password_change = models.BooleanField(default=False, verbose_name=_("Forcer le changement de mot de passe"))
    password_reset_date = models.DateTimeField(null=True, blank=True, verbose_name=_("Date de forçage du reset"))

    # Synchronization fields
    is_sync_enabled = models.BooleanField(default=True, verbose_name=_("Synchronisation activée"))
    last_sync_date = models.DateTimeField(null=True, blank=True, verbose_name=_("Dernière synchronisation"))
    sync_interval_minutes = models.PositiveIntegerField(default=60, verbose_name=_("Intervalle de synchronisation (min)"))
    sync_token = models.CharField(max_length=255, unique=True, null=True, blank=True, verbose_name=_("Token de synchronisation"))

    @property
    def effective_max_upload_size(self):
        """Retourne la limite d'upload effective (Tenant > Global > 400KB)."""
        if self.max_upload_size is not None:
            return self.max_upload_size
        
        try:
            from saas_admin_app.models import SaaSGlobalConfiguration
            return SaaSGlobalConfiguration.get_solo().max_upload_size
        except (ImportError, Exception):
            return 400

    def __str__(self):
        return self.nom
    
class Domaine(DomainMixin):
    pass

class TenantFolder(models.Model):
    sender = models.ForeignKey(Institut, on_delete=models.CASCADE, related_name='sent_folders')
    receiver = models.ForeignKey(Institut, on_delete=models.CASCADE, related_name='received_folders', null=True, blank=True)
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subfolders')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class TenantMessage(models.Model):
    sender = models.ForeignKey(Institut, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(Institut, on_delete=models.CASCADE, related_name='received_messages', null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    attached_file = models.FileField(upload_to='tenant_chat_docs/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"From {self.sender} to {self.receiver} - {self.created_at}"

class TenantDocument(models.Model):
    sender = models.ForeignKey(Institut, on_delete=models.CASCADE, related_name='sent_documents')
    receiver = models.ForeignKey(Institut, on_delete=models.CASCADE, related_name='received_documents', null=True, blank=True)
    file = models.FileField(upload_to='tenant_docs/')
    folder = models.ForeignKey(TenantFolder, on_delete=models.CASCADE, null=True, blank=True, related_name='documents')
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Doc {self.id} from {self.sender}"