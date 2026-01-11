import os
import django
import sys
from django.db import connection

# Add project root to path
sys.path.append(os.getcwd())

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "school.settings")
django.setup()

from app.models import Institut, TenantMessage
from django_tenants.utils import schema_context

def run():
    print("--- Starting Repro ---")
    
    # Get tenants
    master = Institut.objects.filter(tenant_type='master').first()
    second = Institut.objects.filter(nom='bejaia').first() 

    if not master or not second:
        print("Tenants not found.")
        return

    print(f"Master: {master.schema_name} (ID: {master.id}), Second: {second.schema_name} (ID: {second.id})")

    # Create message from Master (Public context)
    msg = TenantMessage.objects.create(
        sender=master,
        receiver=second,
        message="Debug Message from Master"
    )
    print(f"Created message ID: {msg.id} in Public schema.")

    # Check existence in Public
    count_public = TenantMessage.objects.filter(receiver=second).count()
    print(f"Count in Public: {count_public}")

    # Switch to Second context
    print(f"Switching to schema: {second.schema_name}")
    with schema_context(second.schema_name):
        # Check existence in Second context
        count_second = TenantMessage.objects.filter(receiver=second).count()
        print(f"Count in Second Context: {count_second}")
        
        # Verify search path
        with connection.cursor() as cursor:
            cursor.execute("SHOW search_path")
            print(f"Current Search Path: {cursor.fetchone()[0]}")

if __name__ == '__main__':
    run()
