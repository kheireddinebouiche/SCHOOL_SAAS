import os
import django
import sys

sys.path.append(r'c:\Users\kheir\Documents\saldae\SCHOOL_SAAS')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "school.settings") 
django.setup()

from django.db import connection
from django_tenants.utils import get_tenant_model
from t_exam.models import ModelBuilltins, BuiltinTypeNote

Tenant = get_tenant_model()
t = Tenant.objects.get(schema_name='alger')
connection.set_tenant(t)

try:
    # Get active model BTS
    model = ModelBuilltins.objects.filter(label='BTS').first()
    if model:
        print(f"Found active model: {model.label}")
        # Disable has_sous_notes for MCC and EXAM
        for code in ['MCC', 'EXAM']:
            btn = BuiltinTypeNote.objects.filter(builtin=model, code=code).first()
            if btn:
                print(f"Updating {btn.libelle} ({btn.code}): setting has_sous_notes=False, nb_sous_notes=0")
                btn.has_sous_notes = False
                btn.nb_sous_notes = 0
                btn.save()
            else:
                print(f"Could not find type note with code {code} in model {model.label}")
    else:
        print("Model BTS not found.")
except Exception as e:
    import traceback
    traceback.print_exc()
