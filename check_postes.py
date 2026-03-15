import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')
django.setup()

from associe_app.models import PostesBudgetaire
from django_tenants.utils import schema_context

out = []
with schema_context('public'):
    postes = PostesBudgetaire.objects.all().prefetch_related('payment_categories__payment_types', 'depense_categories__payment_category__payment_types')
    for p in postes:
        data = {
            'id': p.id,
            'label': p.label,
            'type': p.type,
            'parent_id': p.parent_id,
            'channels': []
        }
        channels = set()
        if p.type == 'recette':
            for cat in p.payment_categories.all():
                if cat.name:
                    channels.add(cat.name)
        else:
            for cat in p.depense_categories.all():
                if cat.name:
                    channels.add(cat.name)
        data['channels'] = sorted(list(channels))
        out.append(data)

with open('postes_dump.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, indent=2, ensure_ascii=False)
print("Dump completed")
