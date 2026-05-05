import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')
django.setup()

from associe_app.models import BudgetCampaign

print("--- Budget Campaigns ---")
for c in BudgetCampaign.objects.all():
    print(f"ID: {c.id}, Name: {c.name}, Is Active: {c.is_active}")
print("--- End ---")
