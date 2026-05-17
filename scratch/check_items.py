import os
import sys
import django

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')
django.setup()

from django_tenants.utils import schema_context
from associe_app.models import BudgetExtensionRequest, BudgetExtensionItem

with schema_context('public'):
    req = BudgetExtensionRequest.objects.order_by('-created_at').first()
    if req:
        items = BudgetExtensionItem.objects.filter(request=req)
        print(f"Latest Request ID: {req.id} from {req.institut.nom} at {req.created_at}")
        print(f"Items count: {items.count()}")
        for item in items:
            print(f"  - Poste {item.poste.label}: {item.old_amount} -> {item.requested_amount}")
    else:
        print("No requests found.")
