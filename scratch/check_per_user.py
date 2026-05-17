import os
import sys
import django

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')
django.setup()

from django_tenants.utils import schema_context
from associe_app.models import SaaSNotification
from django.contrib.auth.models import User

with schema_context('public'):
    users = list(User.objects.all())
    print(f"Users found in public: {[u.username for u in users]}")
    for u in users:
        print(f"User: {u.username}")
        notifs = SaaSNotification.objects.filter(user=u).order_by('-created_at')
        print(f"  Count: {notifs.count()}")
        for n in notifs[:3]:
            print(f"  - {n.message}")
