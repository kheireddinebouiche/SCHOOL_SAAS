import os
import sys
import django

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')
django.setup()

from associe_app.utils import send_saas_notification
from django_tenants.utils import schema_context
from associe_app.models import SaaSNotification

print("Attempting to send a test notification...")
send_saas_notification("TEST NOTIFICATION FROM SCRATCH", link="/test/")

with schema_context('public'):
    count = SaaSNotification.objects.filter(message="TEST NOTIFICATION FROM SCRATCH").count()
    print(f"Test notifications created: {count}")
