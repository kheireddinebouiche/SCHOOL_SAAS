from django_tenants.utils import schema_context
from t_formations.models import Modules
try:
    with schema_context('alger'):
        modules = Modules.objects.all()[:10]
        print([(m.label, m.code_interne) for m in modules])
except Exception as e:
    print(f"Error: {e}")
