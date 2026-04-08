from django.db import models
from django.utils.translation import gettext_lazy as _

class SaaSEmailConfiguration(models.Model):
    """Configuration email globale pour le SaaS Admin (schéma public)."""
    
    # Email Activation
    email_enabled = models.BooleanField(default=False, verbose_name=_("Envoi d'emails activé"))
    
    # SMTP Settings
    email_host = models.CharField(max_length=255, default='smtp.gmail.com', verbose_name=_("Serveur SMTP"))
    email_port = models.PositiveIntegerField(default=587, verbose_name=_("Port SMTP"))
    email_use_tls = models.BooleanField(default=True, verbose_name=_("Utiliser TLS"))
    email_host_user = models.CharField(max_length=255, default='', verbose_name=_("Email expéditeur"))
    email_host_password = models.CharField(max_length=255, default='', verbose_name=_("Mot de passe email"))
    default_from_email = models.CharField(max_length=255, default='noreply@school-saas.com', verbose_name=_("Email par défaut"))
    
    # Email Templates
    email_reset_password_subject = models.CharField(
        max_length=255, 
        default='Réinitialisation de votre mot de passe - School SaaS', 
        verbose_name=_("Objet - Reset mot de passe")
    )
    email_reset_password_template = models.TextField(
        default='Bonjour {user_name},\n\nVotre mot de passe a été réinitialisé.\n\nVotre nouveau mot de passe est : {password}\n\nVeuillez vous connecter et changer ce mot de passe dès que possible.\n\nCordialement,\nL\'équipe School SaaS',
        verbose_name=_("Template - Reset mot de passe"),
        help_text="Utilisez {user_name} et {password} comme variables"
    )
    
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Configuration Email SaaS"
        verbose_name_plural = "Configuration Email SaaS"

    def __str__(self):
        return "Configuration Email SaaS"

    @classmethod
    def get_solo(cls):
        """Retourne l'unique instance de configuration."""
        obj, created = cls.objects.get_or_create(id=1)
        return obj
    
    def apply_email_settings(self):
        """Applique les paramètres email aux settings Django."""
        from django.conf import settings
        settings.EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
        settings.EMAIL_HOST = self.email_host
        settings.EMAIL_PORT = self.email_port
        settings.EMAIL_USE_TLS = self.email_use_tls
        settings.EMAIL_HOST_USER = self.email_host_user
        settings.EMAIL_HOST_PASSWORD = self.email_host_password
        settings.DEFAULT_FROM_EMAIL = self.default_from_email


class SaaSMaintenanceConfiguration(models.Model):
    """Configuration du mode développement / maintenance global."""
    
    is_maintenance_mode = models.BooleanField(
        default=False, 
        verbose_name=_("Mode Maintenance (En attente) actif")
    )
    maintenance_message = models.TextField(
        default="Nous mettons actuellement la plateforme à jour. Merci de réessayer plus tard.",
        verbose_name=_("Message de maintenance")
    )
    maintenance_end_time = models.DateTimeField(
        null=True, blank=True, 
        verbose_name=_("Heure de fin prévue")
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Configuration Maintenance SaaS"
        verbose_name_plural = "Configuration Maintenance SaaS"

    def __str__(self):
        return "Configuration Maintenance Globale"

    @classmethod
    def get_solo(cls):
        """Retourne l'unique instance de configuration."""
        obj, created = cls.objects.get_or_create(id=1)
        return obj
