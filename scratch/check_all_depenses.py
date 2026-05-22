import os
import django
import sys

sys.path.append(r'c:\Users\kheir\Documents\saldae\SCHOOL_SAAS')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')
django.setup()

from django_tenants.utils import schema_context
from app.models import Institut
from t_tresorerie.models import Depenses, Rembourssements

def check_all_depenses():
    tenant = Institut.objects.exclude(schema_name='public').first()
    if not tenant:
        return

    with schema_context(tenant.schema_name):
        print("All Depenses:")
        for d in Depenses.objects.all():
            print(f"  ID: {d.id}, Label: {d.label}, Client: {d.client}, Montant TTC: {d.montant_ttc}, Created: {d.created_at}")
            
if __name__ == '__main__':
    check_all_depenses()
