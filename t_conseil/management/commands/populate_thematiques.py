from django.core.management.base import BaseCommand
from t_conseil.models import Thematiques

class Command(BaseCommand):
    help = 'Populate Thematiques model with sample data'

    def handle(self, *args, **options):
        data = [
            {
                'label': 'Conseil Stratégique',
                'description': "Accompagnement dans la définition de la stratégie d'entreprise.",
                'prix': 1500.00,
                'duree': 480,
                'billing_type': 'jour'
            },
            {
                'label': 'Audit Organisationnel',
                'description': 'Analyse de la structure et des processus internes.',
                'prix': 2500.00,
                'duree': 960,
                'billing_type': 'jour'
            },
            {
                'label': 'Formation Management',
                'description': 'Session de formation pour les cadres dirigeants.',
                'prix': 500.00,
                'duree': 180,
                'billing_type': 'heure'
            },
            {
                'label': 'Coaching Individuel',
                'description': 'Accompagnement personnalisé pour le développement des compétences.',
                'prix': 150.00,
                'duree': 60,
                'billing_type': 'heure'
            },
            {
                'label': 'Étude de Marché',
                'description': "Analyse sectorielle et recherche d'opportunités.",
                'prix': 3000.00,
                'duree': 1440,
                'billing_type': 'jour'
            },
        ]

        for item in data:
            obj, created = Thematiques.objects.get_or_create(
                label=item['label'],
                defaults={
                    'description': item['description'],
                    'prix': item['prix'],
                    'duree': item['duree'],
                    'billing_type': item['billing_type'],
                    'etat': 'active'
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Successfully created thematic: {item['label']}"))
            else:
                self.stdout.write(self.style.WARNING(f"Thematic already exists: {item['label']}"))
