import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')
django.setup()

from django_tenants.utils import get_tenant_model, schema_context
from t_tresorerie.models import Depenses, Rembourssements, SuiviChequeSortant

TenantModel = get_tenant_model()

total_processed = 0
for tenant in TenantModel.objects.exclude(schema_name='public'):
    with schema_context(tenant.schema_name):
        count_d = 0
        count_r = 0
        
        # Depenses
        depenses = Depenses.objects.filter(mode_paiement='vir')
        for d in depenses:
            statut = 'emis'
            if d.date_paiement or d.lettrages.filter(is_rapproche=True).exists():
                statut = 'decaisse'
            obj, created = SuiviChequeSortant.objects.get_or_create(depense=d, defaults={'statut': statut})
            if created and statut == 'decaisse':
                obj.date_decaisse = d.date_paiement or d.created_at
                obj.save()
            count_d += 1
            
        # Remboursements
        rembs = Rembourssements.objects.filter(mode_rembourssement='vir')
        for r in rembs:
            statut = 'emis'
            is_rapproche = r.lettrages.filter(is_rapproche=True).exists()
            if is_rapproche:
                statut = 'decaisse'
            obj, created = SuiviChequeSortant.objects.get_or_create(remboursement=r, defaults={'statut': statut})
            if created and statut == 'decaisse':
                obj.date_decaisse = r.created_at
                obj.save()
            count_r += 1
            
        if count_d + count_r > 0:
            print(f"Tenant {tenant.schema_name}: processed {count_d} depenses vir, {count_r} remboursements vir")
        total_processed += count_d + count_r

print(f"Backfill virements complete. Total processed: {total_processed}")
