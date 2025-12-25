from t_documents_maker.models import DocumentVariable

# Create default document variables
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

for name, label, description in tags:
    variable, created = DocumentVariable.objects.get_or_create(
        name=name,
        defaults={
            'label': label,
            'description': description,
        }
    )
    if created:
        print(f'Created document variable: {name}')
    else:
        print(f'Document variable already exists: {name}')

print('Document variables setup completed!')