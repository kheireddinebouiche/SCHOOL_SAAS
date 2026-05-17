import os
import django
import sys

sys.path.append(r'c:\Users\kheir\Documents\saldae\SCHOOL_SAAS')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')
django.setup()

from t_tresorerie.models import Paiements

print("Fields in Paiements model:")
for field in Paiements._meta.get_fields():
    print(f"Name: {field.name}, Type: {type(field).__name__}")
