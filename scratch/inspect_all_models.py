import os
import django
import sys

sys.path.append(r'c:\Users\kheir\Documents\saldae\SCHOOL_SAAS')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')
django.setup()

from django.apps import apps

print("ALL MODELS MATCHING 'Paiements':")
for model in apps.get_models():
    if model.__name__.lower() == 'paiements':
        print(f"Model: {model.__name__}, App: {model._meta.app_label}, Fields:")
        for field in model._meta.get_fields():
            print(f"  Field: {field.name}, Type: {type(field).__name__}")

print("\nFIELDS in clientPaiementsRequestLine:")
clientPaiementsRequestLine = apps.get_model('t_tresorerie', 'clientPaiementsRequestLine')
for field in clientPaiementsRequestLine._meta.get_fields():
    print(f"  Field: {field.name}, Type: {type(field).__name__}, Related Model: {getattr(field, 'related_model', None)}")
