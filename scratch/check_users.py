import os
import sys
import django

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')
django.setup()

from django_tenants.utils import schema_context
from django.contrib.auth.models import User

with schema_context('public'):
    users = User.objects.all()
    for u in users:
        print(f"User: {u.username} | Superuser: {u.is_superuser} | Staff: {u.is_staff} | Active: {u.is_active}")
