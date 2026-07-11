import os
import django
import re

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')
django.setup()

from pdf_editor.models import DocumentTemplate
from django_tenants.utils import schema_context
from app.models import Institut

tenant = Institut.objects.get(schema_name='alger')
with schema_context(tenant.schema_name):
    t = DocumentTemplate.objects.get(slug='dolibare')
    content = t.content
    
    # List of variables to add DA to
    vars_to_add_da = [
        r'\{\{\s*ligne\.prix_unitaire\|floatformat:2\s*\}\}',
        r'\{\{\s*ligne\.montant\|floatformat:2\s*\}\}',
        r'\{\{\s*total_ht\|floatformat:2\s*\}\}',
        r'\{\{\s*total_remise\|floatformat:2\s*\}\}',
        r'\{\{\s*total_tva\|floatformat:2\s*\}\}',
        r'\{\{\s*total_ttc\|floatformat:2\s*\}\}'
    ]
    
    for var in vars_to_add_da:
        # Check if " DA" is already there so we don't duplicate
        pattern = var + r'(?!\s*DA)'
        content = re.sub(pattern, lambda m: m.group(0) + ' DA', content)
        
    t.content = content
    t.save()
    print('Modifié avec succès pour ajouter DA!')
