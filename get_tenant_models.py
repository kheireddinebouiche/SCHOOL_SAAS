import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')
django.setup()

from django.apps import apps
from django.conf import settings

tenant_apps = settings.TENANT_APPS
models_list = []

for app_name in tenant_apps:
    if app_name.startswith('django.') or app_name in ['phonenumber_field', 'django_countries', 'taggit', 'pdf_editor']:
        continue
    try:
        app_config = apps.get_app_config(app_name.split('.')[-1])
        for model in app_config.get_models():
            models_list.append({
                'app_label': app_config.label,
                'model_name': model.__name__,
                'verbose_name': str(model._meta.verbose_name).capitalize()
            })
    except LookupError:
        pass

import json
with open('tenant_models.json', 'w', encoding='utf-8') as f:
    json.dump(models_list, f, ensure_ascii=False, indent=2)

print("Saved", len(models_list), "models to tenant_models.json")
