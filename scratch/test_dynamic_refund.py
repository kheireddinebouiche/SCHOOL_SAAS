import os
import django
import sys

sys.path.append(r'c:\Users\kheir\Documents\saldae\SCHOOL_SAAS')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')
django.setup()

from django.db.models import Q, Sum
from django_tenants.utils import schema_context
from app.models import Institut
from t_tresorerie.models import Promos, Paiements, Rembourssements

def test_dynamic():
    tenant = Institut.objects.exclude(schema_name='public').first()
    if not tenant:
        return

    with schema_context(tenant.schema_name):
        promos = list(Promos.objects.filter(etat="active").values('id', 'code', 'session'))
        for promo in promos:
            print(f"\nPromo: {promo['session']} ({promo['code']})")
            
            # 1. Get payments
            payments_qs = Paiements.objects.filter(is_refund=False).filter(
                Q(promo_id=promo['id']) | Q(due_paiements__promo_id=promo['id'])
            ).filter(
                Q(prospect__statut="convertit") | Q(prospect__statut="annuler")
            ).distinct()
            
            total_paye = payments_qs.aggregate(total=Sum('montant_paye'))['total'] or 0
            
            # 2. Get distinct prospects who have made payments for this promo
            prospect_ids = list(payments_qs.values_list('prospect_id', flat=True).distinct())
            print(f"  Prospects with payments in this promo: {prospect_ids}")
            
            # 3. Sum refunds for these prospects
            if prospect_ids:
                total_rembourse = Rembourssements.objects.filter(
                    client_id__in=prospect_ids,
                    is_appliced=True
                ).aggregate(total=Sum('allowed_amount'))['total'] or 0
            else:
                total_rembourse = 0
                
            montant_paye_effectif = float(total_paye) - float(total_rembourse)
            print(f"  Total paye: {total_paye}")
            print(f"  Dynamic total_rembourse: {total_rembourse}")
            print(f"  Dynamic montant_paye (effective): {montant_paye_effectif}")

if __name__ == '__main__':
    test_dynamic()
