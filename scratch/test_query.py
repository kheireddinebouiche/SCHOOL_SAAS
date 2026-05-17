import os
import django
import sys

sys.path.append(r'c:\Users\kheir\Documents\saldae\SCHOOL_SAAS')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')
django.setup()

from t_tresorerie.models import Paiements
from app.models import Institut
from django_tenants.utils import schema_context

tenant = Institut.objects.exclude(schema_name='public').first()
if not tenant:
    tenant = Institut.objects.first()

print("Using tenant schema:", tenant.schema_name)
with schema_context(tenant.schema_name):
    try:
        print("Testing query...")
        listes = Paiements.objects.filter(paiement_line__paiement_request__id=1)
        print("Query executed successfully! Count:", listes.count())
    except Exception as e:
        print("Query failed with error:", e)
