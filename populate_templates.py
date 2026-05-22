import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')
django.setup()

from django.db import connection
from django_tenants.utils import get_tenant_model
from django.utils.text import slugify
from pdf_editor.models import DocumentTemplate

def populate():
    for tenant in get_tenant_model().objects.all():
        schema = tenant.schema_name
        print(f"Creating templates for schema: {schema}")
        try:
            connection.set_schema(schema)
            DEFAULT_CONTENT = {
                'invoice': '<h1>Facture</h1><p>Contenu de la facture.</p>',
                'contract': '<h1>Contrat</h1><p>Contenu du contrat.</p>',
                'certificate': '<h1>Certificat</h1><p>Contenu du certificat.</p>',
                'report': '<h1>Rapport</h1><p>Contenu du rapport.</p>',
                'letter': '<h1>Lettre</h1><p>Contenu de la lettre.</p>',
                'student_info': '<h1>Fiche Étudiant</h1><p>Contenu de la fiche étudiant.</p>',
                'payment_receipt': '<h1>Reçu de Paiement</h1><p>Contenu du reçu.</p>',
                'payment_statement': '<h1>Relevé de Paiement</h1><p>Contenu du relevé.</p>',
            }
            
            created = 0
            for tmpl_type, _display in DocumentTemplate.TEMPLATE_TYPES:
                slug = slugify(tmpl_type)
                if DocumentTemplate.objects.filter(slug=slug).exists():
                    print(f"  Template '{tmpl_type}' already exists, skipping.")
                    continue
                title = f"Template {tmpl_type.title()}"
                content = DEFAULT_CONTENT.get(tmpl_type, '<p>Contenu par défaut.</p>')
                DocumentTemplate.objects.create(
                    title=title,
                    slug=slug,
                    template_type=tmpl_type,
                    content=content,
                    description=f"Template de base pour le type {tmpl_type}.",
                    is_active=True,
                    created_by=None,
                )
                created += 1
                print(f"  Created template '{title}' ({tmpl_type}).")
        except Exception as e:
            print(f"Error on {schema}: {e}")

populate()
