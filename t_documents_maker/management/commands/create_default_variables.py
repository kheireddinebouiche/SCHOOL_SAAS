from django.core.management.base import BaseCommand
from django_tenants.utils import get_tenant_model, get_public_schema_name, schema_context
from t_documents_maker.models import DocumentVariable

class Command(BaseCommand):
    help = 'Create default document variables in all schemas'

    def add_arguments(self, parser):
        parser.add_argument(
            '--schema',
            dest='schema_name',
            help='Specify the schema to create variables in',
        )

    def handle(self, *args, **options):
        schema_name = options.get('schema_name')

        if schema_name:
            # Create variables in specific schema
            self.create_variables_in_schema(schema_name)
        else:
            # Create variables in all schemas
            tenant_model = get_tenant_model()
            for tenant in tenant_model.objects.all():
                self.create_variables_in_schema(tenant.schema_name)

    def create_variables_in_schema(self, schema_name):
        """Create variables in a specific schema"""
        from django.db import connection
        connection.set_schema(schema_name)

        # Define the predefined tags
        tags = [
            ('formation', 'Formation', 'Nom de la formation'),
            ('specialite', 'Spécialité', 'Spécialité de l\'étudiant'),
            ('qualification', 'Qualification', 'Qualification de la formation'),
            ('prix_formation', 'Prix de la formation', 'Prix de la formation'),
            ('annee_academique', 'Année académique', 'Année académique en cours'),
            ('ville', 'Ville', 'Ville de l\'établissement'),
            ('date', 'Date', 'Date du document'),
            ('institut', 'Institut', 'Nom de l\'institut'),
            ('date_naissance_etudiant', 'Date de naissance étudiant', 'Date de naissance de l\'étudiant'),
            ('lieu_naissance_etudiant', 'Lieu de naissance étudiant', 'Lieu de naissance de l\'étudiant'),
            ('adresse_etudiant', 'Adresse étudiant', 'Adresse de l\'étudiant'),
            ('branche', 'Branche', 'Branche de la formation'),
        ]

        created_count = 0
        for name, label, description in tags:
            # Check if variable already exists first
            try:
                variable, created = DocumentVariable.objects.get_or_create(
                    name=name,
                    defaults={
                        'label': label,
                        'description': description,
                    }
                )
                if created:
                    created_count += 1
                    self.stdout.write(f'Created document variable: {name} in schema {schema_name}')
                else:
                    self.stdout.write(f'Document variable already exists: {name} in schema {schema_name}')
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error creating variable {name} in {schema_name}: {str(e)}'))

        self.stdout.write(
            self.style.SUCCESS(f'Successfully processed {created_count} document variables in {schema_name}')
        )