import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')
django.setup()

from django.db import connection
from django_tenants.utils import get_tenant_model
from django.db.migrations.recorder import MigrationRecorder
from pdf_editor.models import DocumentTemplate, DocumentGeneration

def fix_tenants():
    for tenant in get_tenant_model().objects.all():
        schema = tenant.schema_name
        print(f"Fixing schema: {schema}")
        connection.set_schema(schema)
        
        # 1. Ensure the migration is recorded to prevent dependency errors
        recorder = MigrationRecorder(connection)
        recorder.ensure_schema()
        recorder.record_applied("pdf_editor", "0001_initial")
        
        # 2. Check if the table exists, if not create it
        with connection.schema_editor() as schema_editor:
            tables = connection.introspection.table_names()
            if DocumentTemplate._meta.db_table not in tables:
                print(f"Creating table {DocumentTemplate._meta.db_table} for {schema}")
                schema_editor.create_model(DocumentTemplate)
            if DocumentGeneration._meta.db_table not in tables:
                print(f"Creating table {DocumentGeneration._meta.db_table} for {schema}")
                schema_editor.create_model(DocumentGeneration)

fix_tenants()
