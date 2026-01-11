from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Formation
from t_crm.models import UserActionLog
from t_crm.middleware import get_current_user

@receiver(post_save, sender=Formation)
def log_prospect_save(sender, instance, created, **kwargs):
    user = get_current_user()
    action = 'CREATE' if created else 'UPDATE'
    details = f"Formation {instance.nom} {'créé' if created else 'modifié'}."
    
    UserActionLog.objects.create(
        user=user if user and user.is_authenticated else None,
        action_type=action,
        target_model='Formation',
        target_id=str(instance.id),
        details=details
    )

@receiver(post_delete, sender=Formation)
def log_prospect_delete(sender, instance, **kwargs):
    user = get_current_user()
    details = f"Formation {instance.nom} supprimé."
    
    UserActionLog.objects.create(
        user=user if user and user.is_authenticated else None,
        action_type='DELETE',
        target_model='Formation',
        target_id=str(instance.id),
        details=details
    )
