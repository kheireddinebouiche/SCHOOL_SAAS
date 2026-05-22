import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')
django.setup()

from django.db import connection
from django_tenants.utils import get_tenant_model

for tenant in get_tenant_model().objects.all():
    schema = tenant.schema_name
    print(f"Clearing pdf_editor migration for schema: {schema}")
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"SET search_path to {schema}")
            cursor.execute("DELETE FROM django_migrations WHERE app = 'pdf_editor'")
        connection.commit()
    except Exception as e:
        print(f"Error on {schema}: {e}")
