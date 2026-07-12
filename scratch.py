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
    
    # Replace regular space + DA with non-breaking space + DA right after floatformat
    pattern = r'(\{\{.*?floatformat:2\s*\}\})\s*DA'
    
    if re.search(pattern, t.content):
        t.content = re.sub(pattern, r'\1&nbsp;DA', t.content)
        
        # Also ensure the Total columns have white-space: nowrap just in case
        t.content = t.content.replace('width: 40%;">{{ total_ht', 'width: 45%; white-space: nowrap;">{{ total_ht')
        t.content = t.content.replace('width: 40%;">\n<table', 'width: 45%;">\n<table')
        t.content = t.content.replace('width: 60%; vertical-align', 'width: 55%; vertical-align')
        
        # Just add white-space: nowrap to the total TTC row as well
        t.content = t.content.replace('color: #2c3e50;">{{ total_ttc', 'color: #2c3e50; white-space: nowrap;">{{ total_ttc')

        t.save()
        print('Modifié avec succès pour &nbsp; et nowrap!')
    else:
        print('Aucune occurrence trouvée!')
