from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime

def test_details_commission(request):
    """
    Vue de test pour afficher la page de détails de commission avec des données de démonstration
    """
    # Données de démonstration pour les groupes
    groups = [
        {
            'id': 1,
            'name': 'Groupe A - Mathématiques',
            'promotion': 'L3 Mathématiques 2023',
            'exam_subject': 'Mathématiques Avancées',
            'exam_date': datetime.strptime('2023-06-15', '%Y-%m-%d').date(),
            'student_count': 25,
            'status_display': 'En cours',
            'students': [
                {
                    'id': 1,
                    'last_name': 'Dupont',
                    'first_name': 'Jean',
                    'student_id': 'STD001',
                    'grade': 14,
                    'status': 'pass',
                    'status_display': 'Admis'
                },
                {
                    'id': 2,
                    'last_name': 'Martin',
                    'first_name': 'Marie',
                    'student_id': 'STD002',
                    'grade': 16,
                    'status': 'pass',
                    'status_display': 'Admis'
                },
                {
                    'id': 3,
                    'last_name': 'Bernard',
                    'first_name': 'Pierre',
                    'student_id': 'STD003',
                    'grade': 8,
                    'status': 'fail',
                    'status_display': 'Ajourné'
                },
                {
                    'id': 4,
                    'last_name': 'Petit',
                    'first_name': 'Sophie',
                    'student_id': 'STD004',
                    'grade': 12,
                    'status': 'deferred',
                    'status_display': 'Rachat'
                },
                {
                    'id': 5,
                    'last_name': 'Robert',
                    'first_name': 'Michel',
                    'student_id': 'STD005',
                    'grade': None,
                    'status': 'pending',
                    'status_display': 'En attente'
                },
            ]
        },
        {
            'id': 2,
            'name': 'Groupe B - Français',
            'promotion': 'L3 Lettres 2023',
            'exam_subject': 'Littérature Française',
            'exam_date': datetime.strptime('2023-06-18', '%Y-%m-%d').date(),
            'student_count': 18,
            'status_display': 'Programmé',
            'students': [
                {
                    'id': 6,
                    'last_name': 'Richard',
                    'first_name': 'Claire',
                    'student_id': 'STD006',
                    'grade': 15,
                    'status': 'pass',
                    'status_display': 'Admis'
                },
                {
                    'id': 7,
                    'last_name': 'Durand',
                    'first_name': 'Luc',
                    'student_id': 'STD007',
                    'grade': 11,
                    'status': 'deferred',
                    'status_display': 'Rachat'
                },
                {
                    'id': 8,
                    'last_name': 'Leroy',
                    'first_name': 'Anne',
                    'student_id': 'STD008',
                    'grade': 7,
                    'status': 'fail',
                    'status_display': 'Ajourné'
                },
                {
                    'id': 9,
                    'last_name': 'Moreau',
                    'first_name': 'Thomas',
                    'student_id': 'STD009',
                    'grade': 18,
                    'status': 'pass',
                    'status_display': 'Admis'
                },
            ]
        },
        {
            'id': 3,
            'name': 'Groupe C - Informatique',
            'promotion': 'L3 Informatique 2023',
            'exam_subject': 'Algorithmique',
            'exam_date': datetime.strptime('2023-06-20', '%Y-%m-%d').date(),
            'student_count': 30,
            'status_display': 'En cours',
            'students': [
                {
                    'id': 10,
                    'last_name': 'Simon',
                    'first_name': 'Julie',
                    'student_id': 'STD010',
                    'grade': 13,
                    'status': 'pass',
                    'status_display': 'Admis'
                },
                {
                    'id': 11,
                    'last_name': 'Laurent',
                    'first_name': 'Antoine',
                    'student_id': 'STD011',
                    'grade': 9,
                    'status': 'fail',
                    'status_display': 'Ajourné'
                },
                {
                    'id': 12,
                    'last_name': 'Michel',
                    'first_name': 'Catherine',
                    'student_id': 'STD012',
                    'grade': 17,
                    'status': 'pass',
                    'status_display': 'Admis'
                },
                {
                    'id': 13,
                    'last_name': 'Blanc',
                    'first_name': 'Olivier',
                    'student_id': 'STD013',
                    'grade': 10,
                    'status': 'deferred',
                    'status_display': 'Rachat'
                },
                {
                    'id': 14,
                    'last_name': 'Roux',
                    'first_name': 'Nathalie',
                    'student_id': 'STD014',
                    'grade': 14,
                    'status': 'pass',
                    'status_display': 'Admis'
                },
            ]
        },
        {
            'id': 4,
            'name': 'Groupe D - Sciences',
            'promotion': 'L3 Physique 2023',
            'exam_subject': 'Physique Quantique',
            'exam_date': datetime.strptime('2023-06-22', '%Y-%m-%d').date(),
            'student_count': 22,
            'status_display': 'Terminé',
            'students': [
                {
                    'id': 15,
                    'last_name': 'Vincent',
                    'first_name': 'Stéphane',
                    'student_id': 'STD015',
                    'grade': 16,
                    'status': 'pass',
                    'status_display': 'Admis'
                },
                {
                    'id': 16,
                    'last_name': 'Faure',
                    'first_name': 'Isabelle',
                    'student_id': 'STD016',
                    'grade': 12,
                    'status': 'deferred',
                    'status_display': 'Rachat'
                },
                {
                    'id': 17,
                    'last_name': 'Andre',
                    'first_name': 'Eric',
                    'student_id': 'STD017',
                    'grade': 6,
                    'status': 'fail',
                    'status_display': 'Ajourné'
                },
            ]
        }
    ]

    context = {
        'groups': groups
    }

    return render(request, 'tenant_folder/exams/commission/details_commission.html', context)