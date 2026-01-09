from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Prospets, UserActionLog
from .middleware import get_current_user

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
