import os

# We will run this script in django context to update the template directly in DB.
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')
django.setup()

from pdf_editor.models import DocumentTemplate

template = DocumentTemplate.objects.filter(template_type='bulletin', is_active=True).first()
if template:
    # Just need to replace "margin: 1cm" with "margin: 0.5cm"
    if "margin: 1cm;" in template.content:
        template.content = template.content.replace("margin: 1cm;", "margin: 0.5cm;")
        template.save()
        print("Updated template margins in DB.")
    else:
        print("Margin 1cm not found in DB template.")
else:
    print("Template not found.")
