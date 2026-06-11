import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')
django.setup()

from django_tenants.utils import schema_context
from t_conseil.models import LignesFacture
from decimal import Decimal

with schema_context('alger'):
    lines = LignesFacture.objects.filter(prix_unitaire=0, montant_ht__gt=0)
    for l in lines:
        l.prix_unitaire = round(l.montant_ht / l.quantite / (Decimal('1') - (l.remise_percent/Decimal('100'))), 2)
        l.save()
    print(f'Updated {len(lines)} lines')
