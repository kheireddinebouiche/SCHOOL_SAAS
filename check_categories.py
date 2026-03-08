import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')
django.setup()

from associe_app.models import GlobalDepensesCategory

def check_db():
    categories = GlobalDepensesCategory.objects.all().order_by('name')
    print("TOTAL CATEGORIES:", categories.count())
    
    cat_list = []
    for cat in categories:
        cat_data = {
            'id': cat.id,
            'name': cat.name,
            'parent_id': cat.parent.id if cat.parent else None,
            'payment_category': cat.payment_category.name if cat.payment_category else '-',
        }
        print(cat_data)
        cat_list.append(cat_data)

    print("\n--- JSON OUTPUT ---")
    print(json.dumps(cat_list))

if __name__ == '__main__':
    check_db()
