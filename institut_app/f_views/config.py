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
    }
    return render(request, 'tenant_folder/configuration/general_settings.html', context)

@csrf_exempt
@login_required
def api_update_global_settings(request):
    """
    API endpoint to update global settings via AJAX.
    """
    if request.method == 'POST':
        setting_name = request.POST.get('setting_name')
        setting_value = request.POST.get('setting_value') == 'true'
        
        config = GlobalConfiguration.get_solo()
        
        if hasattr(config, setting_name):
            setattr(config, setting_name, setting_value)
            config.save()
            return JsonResponse({'status': 'success', 'message': 'Paramètre mis à jour avec succès.'})
        
        return JsonResponse({'status': 'error', 'message': 'Paramètre non trouvé.'}, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée.'}, status=405)
