from django_tenants.utils import schema_context
from app.models import Institut
from .models import GlobalPaymentCategory, GlobalDepensesCategory, GlobalPaymentType
from t_tresorerie.models import PaymentCategory, DepensesCategory, PaymentType

def sync_global_categories():
    tenants = Institut.objects.exclude(schema_name='public')
    global_payment_cats = GlobalPaymentCategory.objects.all()
    global_depenses_cats = GlobalDepensesCategory.objects.all()
    global_payment_types = GlobalPaymentType.objects.all()

    for tenant in tenants:
        with schema_context(tenant.schema_name):
            # 1. Sync Payment Categories
            # Map names to tenant instances to handle relationships
            payment_cat_map = {} 
            
            # First pass: Create categories without parents
            for g_cat in global_payment_cats:
                # Try to find by global_id first
                p_cat = PaymentCategory.objects.filter(global_id=g_cat.id).first()
                
                # Fallback to name if not found by global_id
                if not p_cat:
                    p_cat = PaymentCategory.objects.filter(name=g_cat.name).first()
                
                if p_cat:
                    # Update existing
                    p_cat.name = g_cat.name
                    p_cat.category_type = g_cat.category_type
                    p_cat.global_id = g_cat.id
                    p_cat.save()
                else:
                    # Create new
                    p_cat = PaymentCategory.objects.create(
                        name=g_cat.name,
                        category_type=g_cat.category_type,
                        global_id=g_cat.id
                    )
                
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
                linked_payment_cat = None
                if g_dep.payment_category:
                     linked_payment_cat = payment_cat_map.get(g_dep.payment_category.id)
                
                # Try to find by global_id first
                d_cat = DepensesCategory.objects.filter(global_id=g_dep.id).first()
                
                # Fallback to name if not found by global_id
                if not d_cat:
                    d_cat = DepensesCategory.objects.filter(name=g_dep.name).first()
                
                if d_cat:
                    # Update existing
                    d_cat.name = g_dep.name
                    d_cat.payment_category = linked_payment_cat
                    d_cat.global_id = g_dep.id
                    d_cat.save()
                else:
                    # Create new
                    d_cat = DepensesCategory.objects.create(
                        name=g_dep.name,
                        payment_category=linked_payment_cat,
                        global_id=g_dep.id
                    )
                
                depense_cat_map[g_dep.id] = d_cat

            # Second pass: Associate parents
            for g_dep in global_depenses_cats:
                if g_dep.parent:
                    d_cat = depense_cat_map.get(g_dep.id)
                    parent_cat = depense_cat_map.get(g_dep.parent.id)
                    if d_cat and parent_cat:
                        d_cat.parent = parent_cat
                        d_cat.save()

            # 3. Sync Payment Types
            for g_type in global_payment_types:
                # Try to find by global_id first
                p_type = PaymentType.objects.filter(global_id=g_type.id).first()
                
                # Fallback to name if not found by global_id
                if not p_type:
                    p_type = PaymentType.objects.filter(name=g_type.name).first()
                
                if p_type:
                    # Update existing
                    p_type.name = g_type.name
                    p_type.global_id = g_type.id
                    p_type.save()
                else:
                    # Create new
                    p_type = PaymentType.objects.create(
                        name=g_type.name,
                        global_id=g_type.id
                    )
                
                # Sync Many-to-Many categories
                cats_to_set = []
                for g_cat in g_type.payment_categories.all():
                    tenant_cat = payment_cat_map.get(g_cat.id)
                    if tenant_cat:
                        cats_to_set.append(tenant_cat)
                
                p_type.payment_categories.set(cats_to_set)
                p_type.save()
