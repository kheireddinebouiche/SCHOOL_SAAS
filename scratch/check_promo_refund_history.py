import os
import django
import sys

sys.path.append(r'c:\Users\kheir\Documents\saldae\SCHOOL_SAAS')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')
django.setup()

from django_tenants.utils import schema_context
from app.models import Institut
from t_tresorerie.models import PromoRembourssement, Depenses, Rembourssements

def check_history():
    tenant = Institut.objects.exclude(schema_name='public').first()
    if not tenant:
        return

    with schema_context(tenant.schema_name):
        print("PromoRembourssements:")
        for pr in PromoRembourssement.objects.all():
            print(f"  ID: {pr.id}, Promo: {pr.promo.session} (ID: {pr.promo.id}), Montant: {pr.montant}, Created: {pr.created_at}, Updated: {pr.updated_at}")
        
        print("\nRemboursements:")
        for r in Rembourssements.objects.all():
            print(f"  ID: {r.id}, Client: {r.client}, Montant: {r.allowed_amount}, Applied: {r.is_appliced}, Created: {r.created_at}")

        print("\nDepenses with Remboursement label:")
        for d in Depenses.objects.filter(label__icontains="Remboursement"):
            print(f"  ID: {d.id}, Client: {d.client}, Montant: {d.montant_ttc}, Created: {d.created_at}")

if __name__ == '__main__':
    check_history()
