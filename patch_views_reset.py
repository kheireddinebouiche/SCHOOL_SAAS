import re

file_path = r'c:\Users\kheir\Documents\saldae\SCHOOL_SAAS\saas_admin_app\views.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

new_view = '''
from django.views.decorators.http import require_POST

@require_POST
def saas_reset_tresorerie_view(request, tenant_id):
    """
    Rinitialise les donnes financires d'un locataire (tenant).
    Purge les tables: Rembourssements, PaiementRemboursement, Depenses, OperationsBancaire, DepotBanque
    """
    from django.http import JsonResponse
    from app.models import Institut
    from django.shortcuts import get_object_or_404
    from django_tenants.utils import tenant_context
    
    institut = get_object_or_404(Institut, id=tenant_id)
    
    try:
        with tenant_context(institut):
            from t_tresorerie.models import (
                Rembourssements, PaiementRemboursement, 
                Depenses, OperationsBancaire, DepotBanque
            )
            
            # Delete in reverse dependency order if any, though Django's CASCADE handles most.
            # We explicitly delete from all 5 models to clear them out.
            PaiementRemboursement.objects.all().delete()
            Rembourssements.objects.all().delete()
            Depenses.objects.all().delete()
            OperationsBancaire.objects.all().delete()
            DepotBanque.objects.all().delete()
            
            return JsonResponse({'status': 'success', 'message': 'La trsorerie a t rinitialise avec succs.'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
'''

if "def saas_reset_tresorerie_view" not in content:
    content += "\n" + new_view
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added saas_reset_tresorerie_view to views.py")
else:
    print("View already exists.")
