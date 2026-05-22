import os
import django
import sys

# Setup Django environment
sys.path.append(r'c:\Users\kheir\Documents\saldae\SCHOOL_SAAS')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')
django.setup()

from django.db.models import Q, Sum
from django_tenants.utils import schema_context
from app.models import Institut
from t_tresorerie.models import Promos, Paiements, DuePaiements, PromoRembourssement
from t_crm.models import Prospets, FicheDeVoeux

def check_payments():
    tenant = Institut.objects.exclude(schema_name='public').first()
    if not tenant:
        print("No tenant found.")
        return

    with schema_context(tenant.schema_name):
        # Let's inspect all payments of all prospects of promo ID 2 (PRJAV24)
        print("--- Inspecting promo ID 2 (PRJAV24) ---")
        p2 = Promos.objects.get(id=2)
        
        # Any payments linked directly to this promo or due_paiements
        all_p = Paiements.objects.filter(
            Q(promo_id=p2.id) | Q(due_paiements__promo_id=p2.id)
        )
        print(f"All payments count: {all_p.count()}")
        for p in all_p:
            print(f"  Payment {p.id}: prospect: {p.prospect} ({p.prospect.statut if p.prospect else 'None'}), is_refund: {p.is_refund}, montant: {p.montant_paye}")
            
        print("\n--- Inspecting all converted prospects of PRJAV24 ---")
        prospects = Prospets.objects.filter(statut="convertit", duepaiements__promo_id=p2.id).distinct()
        print(f"Count of converted prospects: {prospects.count()}")
        for pr in prospects:
            print(f"  Prospect: {pr.nom} {pr.prenom} (statut: {pr.statut})")

        print("\n--- Inspecting promo ID 1 (OCT-25) ---")
        p1 = Promos.objects.get(id=1)
        all_p1 = Paiements.objects.filter(
            Q(promo_id=p1.id) | Q(due_paiements__promo_id=p1.id)
        )
        print(f"All payments count for OCT-25: {all_p1.count()}")
        for p in all_p1:
            print(f"  Payment {p.id}: prospect: {p.prospect} ({p.prospect.statut if p.prospect else 'None'}), is_refund: {p.is_refund}, montant: {p.montant_paye}")

if __name__ == '__main__':
    check_payments()
