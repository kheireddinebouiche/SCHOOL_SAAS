from institut_app.decorators import superuser_required
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from ..models import GlobalConfiguration
from django.views.decorators.csrf import csrf_exempt

@login_required
@superuser_required
def general_settings_view(request):
    """
    Renders the general configuration page.
    """
    from django.contrib.auth import get_user_model
    User = get_user_model()
    config = GlobalConfiguration.get_solo()
    context = {
        'config': config,
        'tenant': request.tenant,
        'users': User.objects.filter(is_active=True).order_by('first_name', 'last_name')
    }
    return render(request, 'tenant_folder/configuration/general_settings.html', context)

from django.db import models

@csrf_exempt
@login_required
@superuser_required
def api_update_global_settings(request):
    """
    API endpoint to update global settings via AJAX.
    """
    if request.method == 'POST':
        setting_name = request.POST.get('setting_name')
        setting_value = request.POST.get('setting_value')
        
        config = GlobalConfiguration.get_solo()
        
        if '__' in setting_name:
            field_name, key_name = setting_name.split('__', 1)
            if hasattr(config, field_name):
                field = config._meta.get_field(field_name)
                if isinstance(field, models.JSONField):
                    current_val = getattr(config, field_name) or {}
                    current_val[key_name] = str(setting_value).lower() == 'true'
                    setattr(config, field_name, current_val)
                    config.save()
                    
                    from t_crm.models import UserActionLog
                    UserActionLog.objects.create(
                        user=request.user,
                        action_type='UPDATE',
                        target_model='GlobalConfiguration',
                        target_id=str(config.id),
                        details=f"Mise à jour du paramètre global {field_name}[{key_name}] = {current_val[key_name]}",
                        ip_address=request.META.get('REMOTE_ADDR')
                    )
                    return JsonResponse({'status': 'success', 'message': 'Paramètre mis à jour avec succès.'})

        if hasattr(config, setting_name):
            # Get the field type to handle conversion
            field = config._meta.get_field(setting_name)
            
            if isinstance(field, models.BooleanField):
                val = str(setting_value).lower() == 'true'
            elif isinstance(field, (models.IntegerField, models.PositiveIntegerField)):
                try:
                    val = int(setting_value) if setting_value else 0
                except (ValueError, TypeError):
                    return JsonResponse({'status': 'error', 'message': 'Valeur numérique invalide.'}, status=400)
            elif isinstance(field, models.ManyToManyField):
                import json
                try:
                    val_list = json.loads(setting_value)
                    getattr(config, setting_name).set(val_list)
                    
                    from t_crm.models import UserActionLog
                    UserActionLog.objects.create(
                        user=request.user,
                        action_type='UPDATE',
                        target_model='GlobalConfiguration',
                        target_id=str(config.id),
                        details=f"Mise à jour du paramètre global (relation multiple) {setting_name}",
                        ip_address=request.META.get('REMOTE_ADDR')
                    )

                    return JsonResponse({'status': 'success', 'message': 'Paramètre mis à jour avec succès.'})
                except Exception as e:
                    return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
            elif isinstance(field, models.JSONField):
                import json
                try:
                    val = json.loads(setting_value)
                except Exception:
                    val = setting_value
            else:
                val = setting_value
                
            setattr(config, setting_name, val)
            config.save()
            
            from t_crm.models import UserActionLog
            UserActionLog.objects.create(
                user=request.user,
                action_type='UPDATE',
                target_model='GlobalConfiguration',
                target_id=str(config.id),
                details=f"Mise à jour du paramètre global {setting_name} = {val}",
                ip_address=request.META.get('REMOTE_ADDR')
            )

            return JsonResponse({'status': 'success', 'message': 'Paramètre mis à jour avec succès.'})
        
        return JsonResponse({'status': 'error', 'message': 'Paramètre non trouvé.'}, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée.'}, status=405)

@csrf_exempt
@login_required
@superuser_required
def api_update_tenant_settings(request):
    """
    API endpoint to update Institut (tenant) details.
    """
    if request.method == 'POST':
        tenant = request.tenant
        nom = request.POST.get('nom')
        adresse = request.POST.get('adresse')
        telephone = request.POST.get('telephone')
        
        if nom:
            tenant.nom = nom
        if adresse is not None:
            tenant.adresse = adresse
        if telephone is not None:
            tenant.telephone = telephone
            
        tenant.save()
        
        from t_crm.models import UserActionLog
        UserActionLog.objects.create(
            user=request.user,
            action_type='UPDATE',
            target_model='Institut',
            target_id=str(tenant.id),
            details=f"Mise à jour des informations de l'établissement {tenant.nom}",
            ip_address=request.META.get('REMOTE_ADDR')
        )

        return JsonResponse({
            'status': 'success', 
            'message': 'Détails de l\'établissement mis à jour avec succès.'
        })
    
    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée.'}, status=405)


@login_required
@superuser_required
def ConfigurationDashboardView(request):
    """
    Renders the main Configuration Dashboard with KPIs and quick links.
    """
    from django.contrib.auth import get_user_model
    from t_crm.models import UserActionLog
    from institut_app.models import Role
    from django.utils import timezone
    from datetime import timedelta

    User = get_user_model()
    
    # KPIs
    total_users = User.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    total_roles = Role.objects.count()
    
    # Active sessions proxy (users with a session key, or you can use your active_sessions logic if it exists)
    # Let's count recent actions as proxy for activity if true sessions are hard to query here
    recent_actions = UserActionLog.objects.order_by('-created_at')[:5]

    context = {
        'total_users': total_users,
        'active_users': active_users,
        'total_roles': total_roles,
        'recent_actions': recent_actions,
        'tenant': request.tenant,
    }

    return render(request, 'tenant_folder/configuration/dashboard.html', context)
