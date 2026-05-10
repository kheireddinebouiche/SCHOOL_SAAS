from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Formation
from t_crm.models import UserActionLog
from t_crm.middleware import get_current_user

@receiver(post_save, sender=Formation)
def log_prospect_save(sender, instance, created, **kwargs):
    user = get_current_user()
    action = 'CREATE' if created else 'UPDATE'
    details = f"Formation {instance.nom} {'créée' if created else 'modifiée'}."
    
    from django.contrib.auth.models import User as AuthUser
    
    # Vérifier si l'utilisateur existe dans le schéma actuel pour éviter IntegrityError (FK violation)
    valid_user = None
    if user and user.is_authenticated:
        if AuthUser.objects.filter(id=user.id).exists():
            valid_user = user

    UserActionLog.objects.create(
        user=valid_user,
        action_type=action,
        target_model='Formation',
        target_id=str(instance.id),
        details=details
    )

@receiver(post_delete, sender=Formation)
def log_prospect_delete(sender, instance, **kwargs):
    user = get_current_user()
    details = f"Formation {instance.nom} supprimée."
    
    from django.contrib.auth.models import User as AuthUser
    
    # Vérifier si l'utilisateur existe dans le schéma actuel pour éviter IntegrityError
    valid_user = None
    if user and user.is_authenticated:
        if AuthUser.objects.filter(id=user.id).exists():
            valid_user = user

    UserActionLog.objects.create(
        user=valid_user,
        action_type='DELETE',
        target_model='Formation',
        target_id=str(instance.id),
        details=details
    )
