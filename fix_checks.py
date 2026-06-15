import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')
django.setup()

from django_tenants.utils import get_tenant_model, schema_context
from t_tresorerie.models import Rembourssements, SuiviChequeSortant

TenantModel = get_tenant_model()

for tenant in TenantModel.objects.exclude(schema_name='public'):
    with schema_context(tenant.schema_name):
        rembs = Rembourssements.objects.filter(mode_rembourssement='che')
        for r in rembs:
            # Re-evaluate
            is_rapproche = r.lettrages.filter(is_rapproche=True).exists()
            if r.is_appliced and not is_rapproche:
                try:
                    sc = SuiviChequeSortant.objects.get(remboursement=r)
                    if sc.statut == 'decaisse':
                        sc.statut = 'emis'
                        sc.date_decaisse = None
                        sc.save()
                        print(f"[{tenant.schema_name}] Reset check for remboursement {r.id} to emis")
                except SuiviChequeSortant.DoesNotExist:
                    pass
