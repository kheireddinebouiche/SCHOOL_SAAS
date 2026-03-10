import os
import django
import sys
import json

sys.path.append(r'c:\Users\kheir\Documents\saldae\SCHOOL_SAAS')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "school.settings") 
django.setup()

from associe_app.models import PostesBudgetaire, GlobalPaymentCategory, GlobalDepensesCategory

data = []
for p in PostesBudgetaire.objects.all():
    parent_label = p.parent.label if p.parent else 'None'
    pay_cats = [{"name": c.name, "parent": c.parent.name if c.parent else "None"} for c in p.payment_categories.all()]
    dep_cats = [{"name": c.name, "parent": c.parent.name if c.parent else "None"} for c in p.depense_categories.all()]
    
    data.append({
        "id": p.id,
        "type": p.type,
        "label": p.label,
        "parent": parent_label,
        "pay_cats": pay_cats,
        "dep_cats": dep_cats
    })

with open('db_dump.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
