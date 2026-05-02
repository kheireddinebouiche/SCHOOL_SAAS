from django_tenants.utils import schema_context
from app.models import Institut
from .models import GlobalPaymentCategory, GlobalDepensesCategory, GlobalPaymentType
from t_tresorerie.models import PaymentCategory, DepensesCategory, PaymentType

def sync_tenant_categories(tenant_schema):
    global_payment_cats = GlobalPaymentCategory.objects.all()
    global_depenses_cats = GlobalDepensesCategory.objects.all()
    global_payment_types = GlobalPaymentType.objects.all()

    with schema_context(tenant_schema):
        # 1. Sync Payment Categories
        payment_cat_map = {} 
        for g_cat in global_payment_cats:
            p_cat = PaymentCategory.objects.filter(global_id=g_cat.id).first()
            if not p_cat:
                p_cat = PaymentCategory.objects.filter(name=g_cat.name).first()
            
            if p_cat:
                p_cat.name = g_cat.name
                p_cat.category_type = g_cat.category_type
                p_cat.description = g_cat.description
                p_cat.global_id = g_cat.id
                p_cat.save()
            else:
                p_cat = PaymentCategory.objects.create(
                    name=g_cat.name,
                    category_type=g_cat.category_type,
                    description=g_cat.description,
                    global_id=g_cat.id
                )
            payment_cat_map[g_cat.id] = p_cat

        for g_cat in global_payment_cats:
            if g_cat.parent:
                p_cat = payment_cat_map.get(g_cat.id)
                parent_cat = payment_cat_map.get(g_cat.parent.id)
                if p_cat and parent_cat:
                    p_cat.parent = parent_cat
                    p_cat.save()

        # 2. Sync Depenses Categories
        depense_cat_map = {}
        for g_dep in global_depenses_cats:
            linked_payment_cat = None
            if g_dep.payment_category:
                 linked_payment_cat = payment_cat_map.get(g_dep.payment_category.id)
            
            d_cat = DepensesCategory.objects.filter(global_id=g_dep.id).first()
            if not d_cat:
                d_cat = DepensesCategory.objects.filter(name=g_dep.name).first()
            
            if d_cat:
                d_cat.name = g_dep.name
                d_cat.payment_category = linked_payment_cat
                d_cat.description = g_dep.description
                d_cat.global_id = g_dep.id
                d_cat.save()
            else:
                d_cat = DepensesCategory.objects.create(
                    name=g_dep.name,
                    payment_category=linked_payment_cat,
                    description=g_dep.description,
                    global_id=g_dep.id
                )
            depense_cat_map[g_dep.id] = d_cat

        for g_dep in global_depenses_cats:
            if g_dep.parent:
                d_cat = depense_cat_map.get(g_dep.id)
                parent_cat = depense_cat_map.get(g_dep.parent.id)
                if d_cat and parent_cat:
                    d_cat.parent = parent_cat
                    d_cat.save()

        # 3. Sync Payment Types
        for g_type in global_payment_types:
            p_type = PaymentType.objects.filter(global_id=g_type.id).first()
            if not p_type:
                p_type = PaymentType.objects.filter(name=g_type.name).first()
            
            if p_type:
                p_type.name = g_type.name
                p_type.global_id = g_type.id
                p_type.save()
            else:
                p_type = PaymentType.objects.create(
                    name=g_type.name,
                    global_id=g_type.id
                )
            
            cats_to_set = []
            for g_cat in g_type.payment_categories.all():
                tenant_cat = payment_cat_map.get(g_cat.id)
                if tenant_cat:
                    cats_to_set.append(tenant_cat)
            
            p_type.payment_categories.set(cats_to_set)
            p_type.save()

def sync_global_categories():
    tenants = Institut.objects.exclude(schema_name='public')
    for tenant in tenants:
        sync_tenant_categories(tenant.schema_name)
