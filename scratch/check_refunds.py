import os
import django
import sys

sys.path.append(r'c:\Users\kheir\Documents\saldae\SCHOOL_SAAS')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')
django.setup()

from django_tenants.utils import schema_context
from app.models import Institut
from t_tresorerie.models import Rembourssements, PaiementRemboursement, Depenses, PromoRembourssement

def check_refunds():
    tenant = Institut.objects.exclude(schema_name='public').first()
    if not tenant:
        return

    with schema_context(tenant.schema_name):
        print("--- All PromoRembourssement records ---")
        for pr in PromoRembourssement.objects.all():
            print(f"PromoRembourssement ID: {pr.id}, Promo: {pr.promo.session} (ID: {pr.promo.id}), Montant: {pr.montant}")
            
        print("\n--- All Rembourssements records ---")
        for r in Rembourssements.objects.all():
            print(f"Remboursement ID: {r.id}, Client: {r.client} (statut: {r.client.statut if r.client else 'None'}), Montant: {r.allowed_amount}, Etat: {r.etat}, Applied: {r.is_appliced}")
            
        print("\n--- All Depenses labelled 'Remboursement' ---")
        for d in Depenses.objects.filter(label__icontains="Remboursement"):
            print(f"Depense ID: {d.id}, Client: {d.client}, Montant TTC: {d.montant_ttc}, Category: {d.category}")

if __name__ == '__main__':
    check_refunds()
