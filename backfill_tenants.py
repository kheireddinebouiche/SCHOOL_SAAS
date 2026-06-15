import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')
django.setup()

from django_tenants.utils import get_tenant_model, schema_context
from t_tresorerie.models import OperationsBancaire, SuiviChequeSortant

TenantModel = get_tenant_model()

for tenant in TenantModel.objects.exclude(schema_name='public'):
    with schema_context(tenant.schema_name):
        ops = OperationsBancaire.objects.filter(operation_type='sortie')
        count = 0
        for op in ops:
            is_cheque = False
            if op.depense and op.depense.mode_paiement == 'che':
                is_cheque = True
            elif op.remboursement and op.remboursement.mode_rembourssement == 'che':
                is_cheque = True
            
            if is_cheque:
                statut = 'emis'
                has_date_paiement = False
                if op.depense and op.depense.date_paiement:
                    has_date_paiement = True
                elif op.remboursement and op.remboursement.is_appliced:
                    has_date_paiement = True
                    
                if has_date_paiement or op.is_rapproche:
                    statut = 'decaisse'
                    
                obj, created = SuiviChequeSortant.objects.get_or_create(operation=op, defaults={'statut': statut})
                if created and statut == 'decaisse':
                    obj.date_decaisse = op.date_operation
                    obj.save()
                
                count += 1
        print(f"Tenant {tenant.schema_name}: processed {count} checks.")

print('Backfill complete across all tenants.')
