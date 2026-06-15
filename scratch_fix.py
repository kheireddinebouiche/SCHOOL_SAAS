import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')
import django
django.setup()
from django.db import connection
connection.set_schema('alger')
from t_tresorerie.models import Paiements, OperationsBancaire
qs = Paiements.objects.filter(prospect__nom='TEST', is_done=False, is_refund=False)
print('Found', qs.count())
for p in qs:
  p.is_refund=True
  p.save()
print('Done')