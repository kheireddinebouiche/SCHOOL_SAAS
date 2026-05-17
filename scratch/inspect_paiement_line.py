import os
import django
import sys

sys.path.append(r'c:\Users\kheir\Documents\saldae\SCHOOL_SAAS')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')
django.setup()

from t_tresorerie.models import Paiements

try:
    field = Paiements._meta.get_field('paiement_line')
    print("Found field 'paiement_line':")
    print("Type:", type(field).__name__)
    print("Related Model:", field.related_model)
    print("Is reverse/forward relation:", field.is_relation)
except Exception as e:
    print("Error getting field 'paiement_line':", e)
