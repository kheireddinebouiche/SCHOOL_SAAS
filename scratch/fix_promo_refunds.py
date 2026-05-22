import os
import django
import sys
from decimal import Decimal

sys.path.append(r'c:\Users\kheir\Documents\saldae\SCHOOL_SAAS')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')
django.setup()

from django.db.models import Sum
from django_tenants.utils import schema_context
from app.models import Institut
from t_formations.models import Promos
from t_crm.models import FicheDeVoeux, FicheVoeuxDouble
from t_tresorerie.models import PromoRembourssement, Rembourssements

def fix_promo_refunds():
    tenant = Institut.objects.exclude(schema_name='public').first()
    if not tenant:
        print("No tenant found.")
        return

    with schema_context(tenant.schema_name):
        print(f"Correcting PromoRembourssement for tenant: {tenant.nom}")
        promos = Promos.objects.all()
        for promo in promos:
            clients_in_promo_standard = FicheDeVoeux.objects.filter(promo_id=promo.id).values_list('prospect_id', flat=True)
            clients_in_promo_double = FicheVoeuxDouble.objects.filter(promo_id=promo.id).values_list('prospect_id', flat=True)
            all_client_ids = set(list(clients_in_promo_standard) + list(clients_in_promo_double))
            
            total_refunds = Rembourssements.objects.filter(
                client_id__in=all_client_ids,
                is_appliced=True
            ).aggregate(total=Sum('allowed_amount'))['total'] or 0
            
            promo_refund, created = PromoRembourssement.objects.get_or_create(promo_id=promo.id)
            old_amount = promo_refund.montant
            promo_refund.montant = Decimal(total_refunds)
            promo_refund.save()
            print(f"  Promo '{promo.session}' (ID: {promo.id}): Corrected from {old_amount} to {promo_refund.montant}")

if __name__ == '__main__':
    fix_promo_refunds()
