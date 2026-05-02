from django_tenants.utils import schema_context
from t_formations.models import Modules
with schema_context('alger'):
    null_count = Modules.objects.filter(code_interne__isnull=True).count()
    empty_count = Modules.objects.filter(code_interne='').count()
    total = Modules.objects.count()
    print(f"Total: {total}, Null: {null_count}, Empty: {empty_count}")
