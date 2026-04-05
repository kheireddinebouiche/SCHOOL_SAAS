from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out
from .models import Prospets, UserActionLog
from .middleware import get_current_user

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    if hasattr(request, 'tenant') and request.tenant.schema_name == 'public':
        return
    ip = get_client_ip(request)
    UserActionLog.objects.create(
        user=user,
        action_type='LOGIN',
        target_model='User',
        target_id=str(user.id),
        details=f"Utilisateur {user.username} s'est connecté.",
        ip_address=ip
    )

@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    if hasattr(request, 'tenant') and request.tenant.schema_name == 'public':
        return
    if user:
        ip = get_client_ip(request)
        UserActionLog.objects.create(
            user=user,
            action_type='LOGOUT',
            target_model='User',
            target_id=str(user.id),
            details=f"Utilisateur {user.username} s'est déconnecté.",
            ip_address=ip
        )

@receiver(post_save, sender=Prospets)
def log_prospect_save(sender, instance, created, **kwargs):
    user = get_current_user()
    action = 'CREATE' if created else 'UPDATE'
    details = f"Prospect {instance.nom} {instance.prenom} {'créé' if created else 'modifié'}."
    
    UserActionLog.objects.create(
        user=user if user and user.is_authenticated else None,
        action_type=action,
        target_model='Prospect',
        target_id=str(instance.id),
        details=details
    )

@receiver(post_delete, sender=Prospets)
def log_prospect_delete(sender, instance, **kwargs):
    user = get_current_user()
    details = f"Prospect {instance.nom} {instance.prenom} supprimé."
    
    UserActionLog.objects.create(
        user=user if user and user.is_authenticated else None,
        action_type='DELETE',
        target_model='Prospect',
        target_id=str(instance.id),
        details=details
    )
