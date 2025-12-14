from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from tenant.models import Tenant, TenantAwareModel  # Remplacer par vos modèles réels si différents
import random
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Crée des données de démonstration pour les commissions d\'examens'

    def handle(self, *args, **options):
        # Créer des groupes d'examens de démonstration
        groups_data = [
            {
                'id': 1,
                'name': 'Groupe A - Mathématiques',
                'promotion': 'L3 Mathématiques 2023',
                'exam_subject': 'Mathématiques Avancées',
                'exam_date': '2023-06-15',
                'student_count': 25,
                'status_display': 'En cours'
            },
            {
                'id': 2,
                'name': 'Groupe B - Français',
                'promotion': 'L3 Lettres 2023',
                'exam_subject': 'Littérature Française',
                'exam_date': '2023-06-18',
                'student_count': 18,
                'status_display': 'Programmé'
            },
            {
                'id': 3,
                'name': 'Groupe C - Informatique',
                'promotion': 'L3 Informatique 2023',
                'exam_subject': 'Algorithmique',
                'exam_date': '2023-06-20',
                'student_count': 30,
                'status_display': 'En cours'
            },
            {
                'id': 4,
                'name': 'Groupe D - Sciences',
                'promotion': 'L3 Physique 2023',
                'exam_subject': 'Physique Quantique',
                'exam_date': '2023-06-22',
                'student_count': 22,
                'status_display': 'Terminé'
            }
        ]

        # Créer des étudiants de démonstration pour chaque groupe
        students_per_group = {
            1: [
                {'last_name': 'Dupont', 'first_name': 'Jean', 'student_id': 'STD001', 'grade': 14, 'status': 'pass', 'status_display': 'Admis'},
                {'last_name': 'Martin', 'first_name': 'Marie', 'student_id': 'STD002', 'grade': 16, 'status': 'pass', 'status_display': 'Admis'},
                {'last_name': 'Bernard', 'first_name': 'Pierre', 'student_id': 'STD003', 'grade': 8, 'status': 'fail', 'status_display': 'Ajourné'},
                {'last_name': 'Petit', 'first_name': 'Sophie', 'student_id': 'STD004', 'grade': 12, 'status': 'deferred', 'status_display': 'Rachat'},
                {'last_name': 'Robert', 'first_name': 'Michel', 'student_id': 'STD005', 'grade': None, 'status': 'pending', 'status_display': 'En attente'},
            ],
            2: [
                {'last_name': 'Richard', 'first_name': 'Claire', 'student_id': 'STD006', 'grade': 15, 'status': 'pass', 'status_display': 'Admis'},
                {'last_name': 'Durand', 'first_name': 'Luc', 'student_id': 'STD007', 'grade': 11, 'status': 'deferred', 'status_display': 'Rachat'},
                {'last_name': 'Leroy', 'first_name': 'Anne', 'student_id': 'STD008', 'grade': 7, 'status': 'fail', 'status_display': 'Ajourné'},
                {'last_name': 'Moreau', 'first_name': 'Thomas', 'student_id': 'STD009', 'grade': 18, 'status': 'pass', 'status_display': 'Admis'},
            ],
            3: [
                {'last_name': 'Simon', 'first_name': 'Julie', 'student_id': 'STD010', 'grade': 13, 'status': 'pass', 'status_display': 'Admis'},
                {'last_name': 'Laurent', 'first_name': 'Antoine', 'student_id': 'STD011', 'grade': 9, 'status': 'fail', 'status_display': 'Ajourné'},
                {'last_name': 'Michel', 'first_name': 'Catherine', 'student_id': 'STD012', 'grade': 17, 'status': 'pass', 'status_display': 'Admis'},
                {'last_name': 'Blanc', 'first_name': 'Olivier', 'student_id': 'STD013', 'grade': 10, 'status': 'deferred', 'status_display': 'Rachat'},
                {'last_name': 'Roux', 'first_name': 'Nathalie', 'student_id': 'STD014', 'grade': 14, 'status': 'pass', 'status_display': 'Admis'},
            ],
            4: [
                {'last_name': 'Vincent', 'first_name': 'Stéphane', 'student_id': 'STD015', 'grade': 16, 'status': 'pass', 'status_display': 'Admis'},
                {'last_name': 'Faure', 'first_name': 'Isabelle', 'student_id': 'STD016', 'grade': 12, 'status': 'deferred', 'status_display': 'Rachat'},
                {'last_name': 'Andre', 'first_name': 'Eric', 'student_id': 'STD017', 'grade': 6, 'status': 'fail', 'status_display': 'Ajourné'},
            ]
        }

        # Ajouter les étudiants aux groupes
        for group in groups_data:
            group['students'] = students_per_group.get(group['id'], [])
        
        # Passer les données à un template de test ou les sauvegarder
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created demo data for {len(groups_data)} groups')
        )
        
        # Afficher un exemple de structure pour le template
        print("\nStructure des données pour le template:")
        print({
            'groups': groups_data
        })