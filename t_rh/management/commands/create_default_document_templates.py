import os
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from pdf_editor.models import DocumentTemplate

# Default HTML content for each template type. In a real project these would be rich HTML templates.
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

class Command(BaseCommand):
    help = 'Create default document templates for each TEMPLATE_TYPE if they do not already exist.'

    def handle(self, *args, **options):
        created = 0
        for tmpl_type, _display in DocumentTemplate.TEMPLATE_TYPES:
            slug = slugify(tmpl_type)
            if DocumentTemplate.objects.filter(slug=slug).exists():
                self.stdout.write(self.style.NOTICE(f"Template '{tmpl_type}' already exists, skipping."))
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
                created_by=None,  # Vous pouvez changer cela selon la logique d'utilisateur.
            )
            created += 1
            self.stdout.write(self.style.SUCCESS(f"Created template '{title}' ({tmpl_type})."))
        self.stdout.write(self.style.SUCCESS(f"Finished. {created} new templates created."))
