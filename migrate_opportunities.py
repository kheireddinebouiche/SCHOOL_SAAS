import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')
django.setup()

from django_tenants.utils import schema_context
from app.models import Institut
from t_crm.models import Prospets, Opportunite

def migrate_prospects_to_opportunities():
    print("Starting migration for all tenants...")
    tenants = Institut.objects.exclude(schema_name='public')
    
    for tenant in tenants:
        print(f"Processing tenant: {tenant.schema_name}")
        with schema_context(tenant.schema_name):
            print(f"Migrating Prospects in {tenant.schema_name}...")
            prospects = Prospets.objects.all()
            count = 0
            for p in prospects:
                if not Opportunite.objects.filter(prospect=p).exists():
                    Opportunite.objects.create(
                        prospect=p,
                        nom=f"Opportunité - {p.nom or ''} {p.prenom or ''}".strip(),
                        stage=p.conseil_pipeline_stage or 'entrant',
                        budget=p.conseil_budget or 0,
                        probability=p.conseil_probability or 0,
                        commercial=p.conseil_commercial,
                        closing_date=p.conseil_closing_date,
                        is_active=p.conseil_is_active,
                        is_favorite=p.conseil_is_favorite
                    )
                    count += 1
            print(f"Successfully migrated {count} prospects in {tenant.schema_name}.")

if __name__ == '__main__':
    migrate_prospects_to_opportunities()
