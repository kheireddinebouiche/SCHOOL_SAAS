import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')
django.setup()

from django_tenants.utils import schema_context
from institut_app.models import UserModuleRole, ModulePermission, Role, Module
from django.contrib.auth import get_user_model

User = get_user_model()

from django_tenants.utils import get_tenant_model, schema_context
from django.db.utils import ProgrammingError

Tenant = get_tenant_model()

found = False
for tenant in Tenant.objects.all():
    try:
        with schema_context(tenant.schema_name):
            attribution = UserModuleRole.objects.first()
            if attribution:
                print(f"--- Schema: {tenant.schema_name} ---")
                print(f"Found attribution: {attribution}")
                perm = ModulePermission.objects.filter(module=attribution.module).first()
                if perm:
                    print(f"Before: is_denied={attribution.denied_permissions.filter(id=perm.id).exists()}")
                    if attribution.denied_permissions.filter(id=perm.id).exists():
                        attribution.denied_permissions.remove(perm)
                        print("Action: removed")
                    else:
                        attribution.denied_permissions.add(perm)
                        print("Action: added")
                    
                    print(f"After: is_denied={attribution.denied_permissions.filter(id=perm.id).exists()}")
                    
                    attribution_refresh = UserModuleRole.objects.get(id=attribution.id)
                    denied_ids = attribution_refresh.denied_permissions.values_list('id', flat=True)
                    print(f"Refreshed QuerySet: {denied_ids}")
                    print(f"Is perm.id in denied_ids? {perm.id in denied_ids}")
                    
                    # Check with list()
                    denied_ids_list = list(denied_ids)
                    print(f"Is perm.id in list(denied_ids)? {perm.id in denied_ids_list}")
                    found = True
                    break
    except ProgrammingError:
        pass
if not found:
    print("No attribution found anywhere")
