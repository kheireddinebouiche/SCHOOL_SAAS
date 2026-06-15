import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')
django.setup()

from django_tenants.utils import get_tenant_model, schema_context
from t_crm.models import Prospets
from django.utils.text import slugify
import uuid

TenantModel = get_tenant_model()

total_fixed = 0

for tenant in TenantModel.objects.all():
    with schema_context(tenant.schema_name):
        try:
            empty = Prospets.objects.filter(slug='')
            count = 0
            for p in empty:
                base = slugify(p.entreprise or 'entreprise')
                if not base:
                    base = 'entreprise'
                p.slug = f"{base}-{str(uuid.uuid4())[:8]}"
                p.save()
                count += 1
            if count > 0:
                print(f"Fixed {count} slugs in tenant {tenant.schema_name}.")
            total_fixed += count
        except Exception as e:
            pass

print(f"Total fixed: {total_fixed} slugs across all tenants.")
