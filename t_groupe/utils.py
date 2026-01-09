from django.shortcuts import get_object_or_404
from t_crm.models import Prospets, FicheDeVoeux, DocumentsDemandeInscription
from t_tresorerie.models import DuePaiements
from t_formations.models import DossierInscription
from django.utils import timezone
from t_groupe.models import GroupeLine

def get_student_context(student_id):
    student = get_object_or_404(Prospets, pk=student_id)

    fiche = get_object_or_404(FicheDeVoeux, prospect=student)
    logo = fiche.specialite.formation.entite_legal.entete_logo.url if fiche.specialite.formation.entite_legal.entete_logo else ''

    specialite = fiche.specialite.label
    formation_label = fiche.specialite.label
    annee_academique = fiche.promo.annee_academique
    echeancier_qs = DuePaiements.objects.filter(client=student, type="frais_f").order_by('date_echeance')
    echeancier = []

    for e in echeancier_qs:
        label = e.label

        if label == "Frais d'inscription":
            label = f"{label} (Non Remboursable)"

        echeancier.append({
            'label': label,
            'montant_due': float(e.montant_due) if e.montant_due is not None else 0.0,
            'date_echeance': e.date_echeance.isoformat() if e.date_echeance else ''
        })

    documents_qs = DossierInscription.objects.filter(formation = fiche.specialite.formation.id)
    documents = []
    for i in documents_qs:
        documents.append({'label' : i.label})

    if not student.is_double:
        current_groupe = GroupeLine.objects.get(student = student, groupe__etat = "inscription" )
    else:
        current_groupe = None

    context_data = {
        'current_date': timezone.now().date().isoformat(),
        'pk': student.pk,
        'nom': student.nom,
        'prenom': student.prenom,
        'photo' : student.photo.url if student.photo else '',
        'date_naissance': student.date_naissance.isoformat() if student.date_naissance else None,
        'lieu_naissance': student.lieu_naissance,
        'email': student.email or '',
        'telephone': student.telephone or '',
        'adresse': student.adresse or '',
        'logo': logo,
        'specialite': specialite,
        'annee_academique': annee_academique,
        'echeancier': echeancier,
        'documents' : documents,
        'formation' : fiche.specialite.formation.nom, # La valeur finale utilisée dans le template
        'groupe': current_groupe.groupe.nom if current_groupe else '',
        'date_entree': fiche.promo.date_debut.isoformat() if fiche.promo and fiche.promo.date_debut else None,
        'date_sortie': fiche.promo.date_fin.isoformat() if fiche.promo and fiche.promo.date_fin else None,
        'matricule' : student.matricule_interne,
        "qualification" : fiche.specialite.formation.qualification,
        "branche" : fiche.specialite.branche,
        "date_debut" : current_groupe.groupe.start_date.isoformat(),
        "date_fin" : current_groupe.groupe.end_date.isoformat(),
    }
    
    return context_data
