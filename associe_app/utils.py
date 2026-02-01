from django_tenants.utils import schema_context
from app.models import Institut
from .models import GlobalPaymentCategory, GlobalDepensesCategory
from t_tresorerie.models import PaymentCategory, DepensesCategory

def sync_global_categories():
    tenants = Institut.objects.exclude(schema_name='public')
    global_payment_cats = GlobalPaymentCategory.objects.all()
    global_depenses_cats = GlobalDepensesCategory.objects.all()

    for tenant in tenants:
        with schema_context(tenant.schema_name):
            # 1. Sync Payment Categories
            # Map names to tenant instances to handle relationships
            payment_cat_map = {} 
            
            # First pass: Create categories without parents
            for g_cat in global_payment_cats:
                p_cat, created = PaymentCategory.objects.get_or_create(
                    name=g_cat.name,
                    defaults={'category_type': g_cat.category_type}
                )
                if not created:
                    p_cat.category_type = g_cat.category_type
                    p_cat.save()
                payment_cat_map[g_cat.id] = p_cat

            # Second pass: Associate parents
            for g_cat in global_payment_cats:
                if g_cat.parent:
                    p_cat = payment_cat_map.get(g_cat.id)
                    parent_cat = payment_cat_map.get(g_cat.parent.id)
                    if p_cat and parent_cat:
                        p_cat.parent = parent_cat
                        p_cat.save()

            # 2. Sync Depenses Categories
            depense_cat_map = {}
            
            # First pass: Create without parents
            for g_dep in global_depenses_cats:
                # Find corresponding payment category if linked
                linked_payment_cat = None
                if g_dep.payment_category:
                     linked_payment_cat = payment_cat_map.get(g_dep.payment_category.id)
                
                d_cat, created = DepensesCategory.objects.get_or_create(
                    name=g_dep.name,
                    defaults={'payment_category': linked_payment_cat}
                )
                if not created:
                     d_cat.payment_category = linked_payment_cat
                     d_cat.save()
                depense_cat_map[g_dep.id] = d_cat

            # Second pass: Associate parents
            for g_dep in global_depenses_cats:
                if g_dep.parent:
                    d_cat = depense_cat_map.get(g_dep.id)
                    parent_cat = depense_cat_map.get(g_dep.parent.id)
                    if d_cat and parent_cat:
                        d_cat.parent = parent_cat
                        d_cat.save()
