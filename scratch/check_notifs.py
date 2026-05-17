import os
import sys
import django

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')
django.setup()

from django_tenants.utils import schema_context
from associe_app.models import SaaSNotification, BudgetExtensionRequest
from django.contrib.auth.models import User

with schema_context('public'):
    notif_count = SaaSNotification.objects.count()
    request_count = BudgetExtensionRequest.objects.count()
    
    print(f"Total Notifications: {notif_count}")
    print(f"Total Extension Requests: {request_count}")
    
    last_requests = BudgetExtensionRequest.objects.order_by('-created_at')[:5]
    for r in last_requests:
        print(f"[{r.created_at}] From {r.institut.nom}: {r.status} (Motif: {r.motif[:30]}...)")

    last_notifs = SaaSNotification.objects.order_by('-created_at')[:5]
    for n in last_notifs:
        print(f"[{n.created_at}] To {n.user.username}: {n.message}")
