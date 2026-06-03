from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import (
    SessionExam, SessionExamLine, ExamPlanification, ModelBuilltins,
    NoteBloc, BuiltinTypeNote, BuiltinTypeNoteDependency, BuiltinSousNote,
    Commissions, CommisionResult, PvExamen, ExamTypeNote,
    ExamTypeNoteDependency, ExamNote, ExamSousNote, ExamDecisionEtudiant,
    DeliberationEtudiant
)
from t_crm.models import UserActionLog
from t_crm.middleware import get_current_user, get_current_request

def get_client_ip(request):
    if not request:
        return None
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def log_exam_action_save(sender, instance, created, **kwargs):
    user = get_current_user()
    request = get_current_request()
    ip = get_client_ip(request)
    action = 'CREATE' if created else 'UPDATE'
    details = f"{sender.__name__} {'créé' if created else 'modifié'}: {str(instance)}"
    
    UserActionLog.objects.create(
        user=user if user and user.is_authenticated else None,
        action_type=action,
        target_model=sender.__name__,
        target_id=str(instance.id) if hasattr(instance, 'id') else '',
        details=details,
        ip_address=ip
    )

def log_exam_action_delete(sender, instance, **kwargs):
    user = get_current_user()
    request = get_current_request()
    ip = get_client_ip(request)
    details = f"{sender.__name__} supprimé: {str(instance)}"
    
    UserActionLog.objects.create(
        user=user if user and user.is_authenticated else None,
        action_type='DELETE',
        target_model=sender.__name__,
        target_id=str(instance.id) if hasattr(instance, 'id') else '',
        details=details,
        ip_address=ip
    )

MODELS_TO_TRACK = [
    SessionExam, SessionExamLine, ExamPlanification, ModelBuilltins,
    NoteBloc, BuiltinTypeNote, BuiltinTypeNoteDependency, BuiltinSousNote,
    Commissions, CommisionResult, PvExamen, ExamTypeNote,
    ExamTypeNoteDependency, ExamNote, ExamSousNote, ExamDecisionEtudiant,
    DeliberationEtudiant
]

for model in MODELS_TO_TRACK:
    post_save.connect(log_exam_action_save, sender=model)
    post_delete.connect(log_exam_action_delete, sender=model)
