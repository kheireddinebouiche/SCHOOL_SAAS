import os
import django
import sys

# Setup Django environment
sys.path.append(r'c:\Users\kheir\Documents\saldae\SCHOOL_SAAS')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')
django.setup()

from django.db.models import Q, Sum
from django.utils.timezone import now
from django_tenants.utils import schema_context
from app.models import Institut
from t_tresorerie.models import Promos, Paiements, DuePaiements, PromoRembourssement
from t_crm.models import Prospets, FicheDeVoeux

def check_promos():
    tenant = Institut.objects.exclude(schema_name='public').first()
    if not tenant:
        print("No tenant found.")
        return

    print(f"Using tenant: {tenant.nom} ({tenant.schema_name})")
    
    with schema_context(tenant.schema_name):
        promos = list(Promos.objects.filter(etat="active").values('id', 'code', 'begin_year', 'end_year', 'session'))
        for promo in promos:
            print(f"\n======================================")
            print(f"Promo: {promo['session']} ({promo['code']}) [ID: {promo['id']}]")
            
            # Total à payer
            total_a_payer = DuePaiements.objects.filter(
                promo_id=promo['id'],
                client__statut="convertit",
                is_annulated=False
            ).aggregate(total=Sum('montant_due'))['total'] or 0
            
            # payments_qs as in the view
            payments_qs = Paiements.objects.filter(is_refund=False).filter(
                Q(promo_id=promo['id']) | Q(due_paiements__promo_id=promo['id'])
            ).filter(
                Q(prospect__statut="convertit") | Q(prospect__statut="annuler")
            ).distinct()
            
            total_paye = payments_qs.aggregate(total=Sum('montant_paye'))['total'] or 0
            
            # total_rembourse
            total_rembourse = PromoRembourssement.objects.filter(promo_id=promo['id']).aggregate(total=Sum('montant'))['total'] or 0
            
            # actual display paye
            montant_paye = float(total_paye) - float(total_rembourse)
            
            print(f"  total_a_payer: {total_a_payer}")
            print(f"  total_paye (Paiements Sum): {total_paye} (from {payments_qs.count()} payments)")
            print(f"  total_rembourse (PromoRembourssement): {total_rembourse}")
            print(f"  calculated montant_paye: {montant_paye}")
            
            # Check if there are PromoRembourssement entries in general
            all_rembs = PromoRembourssement.objects.filter(promo_id=promo['id'])
            print(f"  PromoRembourssement objects for this promo: {list(all_rembs.values())}")

if __name__ == '__main__':
    check_promos()
