import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')
django.setup()

from associe_app.models import BudgetCampaign
from app.models import Institut

print(f"Total campaigns: {BudgetCampaign.objects.count()}")
active_campaign = BudgetCampaign.objects.filter(is_active=True).first()
print(f"Active campaign: {active_campaign}")

if not active_campaign:
    print("No active campaign found. Redirecting to 'mise en route' is expected behavior.")
    # Check if there are any campaigns at all
    if BudgetCampaign.objects.count() == 0:
        print("Creating a default campaign for testing...")
        from datetime import date, timedelta
        # Get an institute to link if necessary (though campaign is global)
        # BudgetCampaign doesn't seem to have a mandatory institute in the model (checking)
        try:
            campaign = BudgetCampaign.objects.create(
                name="Campagne 2025-2026",
                date_debut=date(2025, 8, 1),
                date_fin=date(2026, 7, 31),
                is_active=True,
                target_revenue=1000000
            )
            print(f"Created campaign: {campaign}")
        except Exception as e:
            print(f"Failed to create campaign: {e}")
else:
    print(f"Active campaign found: {active_campaign.name}")
