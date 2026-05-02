import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SCHOOL_SAAS.settings')
django.setup()

from t_formations.models import Specialites, Modules

def check_modules(spec_id):
    modules = Modules.objects.filter(specialite_id=spec_id, is_archived=False).values('id', 'label','code','code_interne','coef','duree', 'est_valider')
    print(json.dumps(list(modules), indent=2))

if __name__ == "__main__":
    # Get the last specialty for testing
    spec = Specialites.objects.last()
    if spec:
        print(f"Checking modules for specialty: {spec.label} (ID: {spec.id})")
        check_modules(spec.id)
    else:
        print("No specialty found")
