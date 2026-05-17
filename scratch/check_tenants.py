import os
import sys
import django

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')
django.setup()

from django_tenants.utils import get_tenant_model, get_tenant_domain_model

Tenant = get_tenant_model()
Domain = get_tenant_domain_model()

print("Tenants:")
for t in Tenant.objects.all():
    print(f"  - {t.schema_name} (Type: {t.get_tenant_type_display() if hasattr(t, 'get_tenant_type_display') else 'N/A'})")
    domains = Domain.objects.filter(tenant=t)
    for d in domains:
        print(f"    * Domain: {d.domain} (Primary: {d.is_primary})")
