import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')
django.setup()
from django_tenants.utils import schema_context
from t_crm.models import Prospets
from t_tresorerie.models import Paiements
with schema_context('alger'):
    for p in Prospets.objects.filter(nom='TEST'):
        print(f'Prospet ID: {p.id}, prenom: {p.prenom}, statut: {p.statut}, paid: {Paiements.objects.filter(prospect=p).count()} payments')
