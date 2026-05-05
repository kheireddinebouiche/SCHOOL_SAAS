import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')
django.setup()

from associe_app.models import BudgetCampaign

campaign = BudgetCampaign.objects.filter(name="Budget 2025-2026").first()
if campaign:
    campaign.is_active = True
    campaign.save()
    print(f"Campaign {campaign.name} set to active.")
else:
    print("Campaign not found.")
