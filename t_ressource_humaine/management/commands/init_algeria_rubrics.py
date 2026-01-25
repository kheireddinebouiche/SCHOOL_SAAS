
from django.core.management.base import BaseCommand
from t_ressource_humaine.models import Rubrique

class Command(BaseCommand):
    help = 'Initializes common Algerian payroll rubrics (primes)'

    def handle(self, *args, **options):
        # List of common rubrics
        # Format: (libelle, type_rubrique, est_cotisable, est_imposable)
        rubriques_data = [
            ("Indemnité d'Expérience Professionnelle (IEP)", 'GAIN', True, True),
            ("Prime de Rendement Collectif (PRC)", 'GAIN', True, True),
            ("Prime de Rendement Individuel (PRI)", 'GAIN', True, True),
            ("Prime de Nuisance", 'GAIN', True, True),
            ("Prime de Danger", 'GAIN', True, True),
            ("Prime d'Astreinte", 'GAIN', True, True),
            ("Prime de Panier (Cotisable)", 'GAIN', True, True),
            ("Prime de Transport (Cotisable)", 'GAIN', True, True),
            ("Indemnité de Panier (Non Cotisable)", 'GAIN', False, False),
            ("Indemnité de Transport (Non Cotisable)", 'GAIN', False, False),
            ("Indemnité de Zone", 'GAIN', True, True),
            ("Heures Supplémentaires 50%", 'GAIN', True, True),
            ("Heures Supplémentaires 75%", 'GAIN', True, True),
            ("Retenue Absence", 'RETENUE', False, False),
            ("Retenue Retard", 'RETENUE', False, False),
            ("Acompte sur Salaire", 'RETENUE', False, False),
            ("Remboursement Prêt", 'RETENUE', False, False),
            ("Cotisation Mutuelle", 'RETENUE', False, False), # Often reducing taxable base? Logic engine treats RETENUE as net deduction for now.
        ]

        created_count = 0
        for libelle, type_r, cotisable, imposable in rubriques_data:
            rubrique, created = Rubrique.objects.get_or_create(
                libelle=libelle,
                defaults={
                    'type_rubrique': type_r,
                    'est_cotisable': cotisable,
                    'est_imposable': imposable,
                    'actif': True
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created rubric: {libelle}'))
                created_count += 1
            else:
                self.stdout.write(f'Rubric already exists: {libelle}')

        self.stdout.write(self.style.SUCCESS(f'Successfully initialized {created_count} new rubrics.'))
