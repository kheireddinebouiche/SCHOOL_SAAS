from django_tenants.utils import schema_context
from t_formations.models import Specialites
with schema_context('alger'):
    null_count = Specialites.objects.filter(code__isnull=True).count()
    empty_count = Specialites.objects.filter(code='').count()
    total = Specialites.objects.count()
    print(f"Total: {total}, Null: {null_count}, Empty: {empty_count}")
