# pdf_editor/variables.py

# Dictionnaire regroupant les variables disponibles pour chaque type de modèle
TEMPLATE_VARIABLES = {
    'contract': [
        {'category': 'Entreprise', 'vars': [
            {'tag': '{{ entreprise.designation }}', 'desc': 'Nom de l\'entreprise'},
            {'tag': '{{ entreprise.adresse }}', 'desc': 'Adresse de l\'entreprise'},
            {'tag': '{{ entreprise.rc }}', 'desc': 'Registre de Commerce (RC)'},
            {'tag': '{{ entreprise.nif }}', 'desc': 'NIF'},
            {'tag': '{{ entreprise.nis }}', 'desc': 'NIS'},
            {'tag': '{{ entreprise.art }}', 'desc': 'Article d\'imposition'},
            {'tag': '{{ entreprise.rib }}', 'desc': 'RIB bancaire'},
        ]},
        {'category': 'Employé', 'vars': [
            {'tag': '{{ employe.civilite|title }}', 'desc': 'Civilité (Mr, Mme, etc.)'},
            {'tag': '{{ employe.nom }}', 'desc': 'Nom de famille'},
            {'tag': '{{ employe.prenom }}', 'desc': 'Prénom'},
            {'tag': '{{ employe.adresse }}', 'desc': 'Adresse personnelle'},
            {'tag': '{{ employe.date_naissance|date:"d/m/Y" }}', 'desc': 'Date de naissance'},
            {'tag': '{{ employe.lieu_naissance }}', 'desc': 'Lieu de naissance'},
            {'tag': '{{ employe.cin }}', 'desc': 'N° CIN / Pièce d\'identité'},
            {'tag': '{{ employe.secu }}', 'desc': 'N° Sécurité Sociale'},
        ]},
        {'category': 'Contrat', 'vars': [
            {'tag': '{{ contrat.poste.label }}', 'desc': 'Titre du poste'},
            {'tag': '{{ contrat.service.label }}', 'desc': 'Département / Service'},
            {'tag': '{{ contrat.date_embauche|date:"d/m/Y" }}', 'desc': 'Date d\'embauche'},
            {'tag': '{{ contrat.duree }}', 'desc': 'Durée (en mois)'},
            {'tag': '{{ contrat.salaire_base }}', 'desc': 'Salaire de base (DA)'},
        ]},
        {'category': 'Divers', 'vars': [
            {'tag': '{{ date_impression }}', 'desc': 'Date d\'impression (Aujourd\'hui)'},
            {'tag': '{{ current_user }}', 'desc': 'Utilisateur ayant généré le document'},
        ]}
    ],
    'invoice': [
        {'category': 'Entreprise', 'vars': [
            {'tag': '{{ entreprise.designation }}', 'desc': 'Nom de l\'entreprise'},
            {'tag': '{{ entreprise.adresse }}', 'desc': 'Adresse de l\'entreprise'},
            {'tag': '{{ entreprise.rc }}', 'desc': 'RC'},
            {'tag': '{{ entreprise.nif }}', 'desc': 'NIF'},
            {'tag': '{{ entreprise.nis }}', 'desc': 'NIS'},
            {'tag': '{{ entreprise.rib }}', 'desc': 'RIB'},
        ]},
        {'category': 'Client', 'vars': [
            {'tag': '{{ client.nom }}', 'desc': 'Nom du client'},
            {'tag': '{{ client.prenom }}', 'desc': 'Prénom du client'},
            {'tag': '{{ client.adresse }}', 'desc': 'Adresse du client'},
            {'tag': '{{ client.telephone }}', 'desc': 'N° de téléphone'},
            {'tag': '{{ client.email }}', 'desc': 'Adresse e-mail'},
        ]},
        {'category': 'Facture', 'vars': [
            {'tag': '{{ facture.num_facture }}', 'desc': 'Numéro de la facture'},
            {'tag': '{{ facture.date_facture|date:"d/m/Y" }}', 'desc': 'Date d\'émission'},
            {'tag': '{{ facture.montant_ht }}', 'desc': 'Montant HT'},
            {'tag': '{{ facture.montant_tva }}', 'desc': 'Montant TVA'},
            {'tag': '{{ facture.montant_ttc }}', 'desc': 'Montant TTC'},
            {'tag': '{{ facture.montant_lettre }}', 'desc': 'Montant en toutes lettres'},
            {'tag': '{{ facture.get_status_display }}', 'desc': 'Statut de la facture (Payée, etc.)'},
        ]},
        {'category': 'Divers', 'vars': [
            {'tag': '{{ date_impression }}', 'desc': 'Date d\'impression'},
        ]}
    ],
    'student_info': [
        {'category': 'Entreprise', 'vars': [
            {'tag': '{{ entreprise.designation }}', 'desc': 'Nom de l\'institut'},
            {'tag': '{{ entreprise.adresse }}', 'desc': 'Adresse'},
        ]},
        {'category': 'Étudiant', 'vars': [
            {'tag': '{{ etudiant.nom }}', 'desc': 'Nom'},
            {'tag': '{{ etudiant.prenom }}', 'desc': 'Prénom'},
            {'tag': '{{ etudiant.matricule }}', 'desc': 'Numéro d\'inscription / Matricule'},
            {'tag': '{{ etudiant.date_naissance|date:"d/m/Y" }}', 'desc': 'Date de naissance'},
            {'tag': '{{ etudiant.lieu_naissance }}', 'desc': 'Lieu de naissance'},
            {'tag': '{{ etudiant.adresse }}', 'desc': 'Adresse'},
        ]},
        {'category': 'Formation', 'vars': [
            {'tag': '{{ promo.specialite.label }}', 'desc': 'Spécialité / Formation'},
            {'tag': '{{ promo.label }}', 'desc': 'Promotion'},
            {'tag': '{{ promo.date_debut|date:"d/m/Y" }}', 'desc': 'Date début formation'},
            {'tag': '{{ promo.date_fin|date:"d/m/Y" }}', 'desc': 'Date fin formation'},
        ]}
    ],
    'certificate': [
        {'category': 'Étudiant', 'vars': [
            {'tag': '{{ etudiant.nom }}', 'desc': 'Nom'},
            {'tag': '{{ etudiant.prenom }}', 'desc': 'Prénom'},
            {'tag': '{{ etudiant.date_naissance|date:"d/m/Y" }}', 'desc': 'Date de naissance'},
            {'tag': '{{ etudiant.lieu_naissance }}', 'desc': 'Lieu de naissance'},
        ]},
        {'category': 'Formation / Attestation', 'vars': [
            {'tag': '{{ promo.specialite.label }}', 'desc': 'Spécialité'},
            {'tag': '{{ promo.label }}', 'desc': 'Promotion'},
            {'tag': '{{ date_impression }}', 'desc': 'Date de délivrance'},
        ]},
        {'category': 'Entreprise', 'vars': [
            {'tag': '{{ entreprise.designation }}', 'desc': 'Nom de l\'institut'},
            {'tag': '{{ entreprise.adresse }}', 'desc': 'Adresse'},
        ]}
    ],
    'payment_receipt': [
        {'category': 'Paiement', 'vars': [
            {'tag': '{{ paiement.num }}', 'desc': 'N° Reçu / Réf'},
            {'tag': '{{ paiement.date_paiement|date:"d/m/Y" }}', 'desc': 'Date de paiement'},
            {'tag': '{{ paiement.montant_paye }}', 'desc': 'Montant (DA)'},
            {'tag': '{{ paiement.get_mode_paiement_display }}', 'desc': 'Mode de paiement (Espèces, etc.)'},
        ]},
        {'category': 'Candidat / Prospect', 'vars': [
            {'tag': '{{ prospect.nom }}', 'desc': 'Nom'},
            {'tag': '{{ prospect.prenom }}', 'desc': 'Prénom'},
        ]},
        {'category': 'Divers', 'vars': [
            {'tag': '{{ current_user }}', 'desc': 'Agent de recouvrement'},
        ]}
    ]
}

def get_variables_for_type(template_type):
    return TEMPLATE_VARIABLES.get(template_type, [])
