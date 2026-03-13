import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_saas.settings')
django.setup()

from associe_app.models import BudgetCampaign

print("Starting backfill of BudgetCampaign slugs...")
campaigns = BudgetCampaign.objects.all()
count = 0
for campaign in campaigns:
    if not campaign.slug:
        campaign.save()  # This triggers the save method which generates the slug
        count += 1
        print(f"Updated {campaign.name} -> {campaign.slug}")

print(f"Finished. Updated {count} campaigns.")
