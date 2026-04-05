from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from ..models import GlobalConfiguration
from django.views.decorators.csrf import csrf_exempt

@login_required
def general_settings_view(request):
    """
    Renders the general configuration page.
    """
    config = GlobalConfiguration.get_solo()
    context = {
        'config': config,
        'tenant': request.tenant,
    }
    return render(request, 'tenant_folder/configuration/general_settings.html', context)

from django.db import models

@csrf_exempt
@login_required
def api_update_global_settings(request):
    """
    API endpoint to update global settings via AJAX.
    """
    if request.method == 'POST':
        setting_name = request.POST.get('setting_name')
        setting_value = request.POST.get('setting_value')
        
        config = GlobalConfiguration.get_solo()
        
        if hasattr(config, setting_name):
            # Get the field type to handle conversion
            field = config._meta.get_field(setting_name)
            
            if isinstance(field, models.BooleanField):
                val = setting_value.lower() == 'true'
            elif isinstance(field, (models.IntegerField, models.PositiveIntegerField)):
                try:
                    val = int(setting_value)
                except (ValueError, TypeError):
                    return JsonResponse({'status': 'error', 'message': 'Valeur numérique invalide.'}, status=400)
            else:
                val = setting_value
                
            setattr(config, setting_name, val)
            config.save()
            return JsonResponse({'status': 'success', 'message': 'Paramètre mis à jour avec succès.'})
        
        return JsonResponse({'status': 'error', 'message': 'Paramètre non trouvé.'}, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée.'}, status=405)

@csrf_exempt
@login_required
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
        return JsonResponse({
            'status': 'success', 
            'message': 'Détails de l\'établissement mis à jour avec succès.'
        })
    
    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée.'}, status=405)
