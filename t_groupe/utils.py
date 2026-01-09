from django.shortcuts import get_object_or_404
from t_crm.models import Prospets, FicheDeVoeux, DocumentsDemandeInscription, FicheVoeuxDouble
from t_tresorerie.models import DuePaiements
from t_formations.models import DossierInscription
from django.utils import timezone
from t_groupe.models import GroupeLine, Groupe

def get_student_context(student_id, group_id=None):
    student = get_object_or_404(Prospets, pk=student_id)

    # Déterminer le groupe actuel
    current_groupe = None
    if group_id:
        current_groupe = Groupe.objects.filter(pk=group_id).first()
    
    if not current_groupe and not student.is_double:
        # Fallback pour les étudiants normaux si group_id pas fourni
        groupe_line = GroupeLine.objects.filter(student=student, groupe__etat="inscription").first()
        if groupe_line:
            current_groupe = groupe_line.groupe

    # Récupération de la fiche et des infos de formation
    logo = ''
    specialite_label = ''
    formation_label = ''
    annee_academique = ''
    qualification = ''
    branche = ''
    documents_qs = []
    
    # Dates
    date_entree = None
    date_sortie = None
    
    montant_specialite = 0.0

    fiche = None

    if student.is_double:
        fiche = FicheVoeuxDouble.objects.filter(prospect=student).first()
        # Si pas de fiche double trouvée, on essaie la fiche normale par sécurité
        if not fiche:
            fiche = get_object_or_404(FicheDeVoeux, prospect=student)

        # Pour les doubles, on s'appuie fortement sur le groupe pour le contexte formation
        if isinstance(fiche, FicheVoeuxDouble) and current_groupe:
            
            # Validation : on vérifie que le groupe correspond bien à l'une des spécialités du double diplôme
            double_diplome = fiche.specialite
            is_valid_group = False
            
            if double_diplome:
                 if current_groupe.specialite == double_diplome.specialite1 or current_groupe.specialite == double_diplome.specialite2:
                     is_valid_group = True
            
            if is_valid_group:
                formation_obj = current_groupe.specialite.formation
                
                logo = formation_obj.entite_legal.entete_logo.url if formation_obj.entite_legal.entete_logo else ''
                specialite_label = current_groupe.specialite.label 
                formation_label = formation_obj.nom
                
                if fiche.promo:
                     annee_academique = fiche.promo.annee_academique
                     date_entree = fiche.promo.date_debut
                     date_sortie = fiche.promo.date_fin
                
                documents_qs = DossierInscription.objects.filter(formation=formation_obj.id)
                qualification = formation_obj.qualification
                branche = current_groupe.specialite.branche

                if current_groupe.specialite == double_diplome.specialite1:
                    montant_specialite = double_diplome.prix_spec1
                elif current_groupe.specialite == double_diplome.specialite2:
                    montant_specialite = double_diplome.prix_spec2
            else:
                # Le groupe ne correspond pas au double diplôme de l'étudiant
                # On peut logger ou laisser vide ? 
                # On va tenter de remplir avec la spécialité du groupe quand même si on est dans une logique forcée, 
                # mais le User a demandé de comparer. Si ça match pas, on risque d'imprimer des trucs faux.
                # On laisse vide ou on met un warning ? 
                # Pour l'instant on ne remplit pas les infos formation si pas de match.
                pass

        elif isinstance(fiche, FicheVoeuxDouble):
             # Cas limite : double sans groupe contexte (affichage minimal)
             specialite_label = fiche.specialite.label if fiche.specialite else ''
             if fiche.promo:
                 annee_academique = fiche.promo.annee_academique
    
    else:
        # Cas standard
        try:
            fiche = FicheDeVoeux.objects.get(prospect=student)
        except FicheDeVoeux.DoesNotExist:
             # Gestion erreur ou fiche vide
             pass
        
        if fiche:
            formation_obj = fiche.specialite.formation
            logo = formation_obj.entite_legal.entete_logo.url if formation_obj.entite_legal.entete_logo else ''
            specialite_label = fiche.specialite.label
            formation_label = formation_obj.nom
            annee_academique = fiche.promo.annee_academique
            
            date_entree = fiche.promo.date_debut
            date_sortie = fiche.promo.date_fin

            documents_qs = DossierInscription.objects.filter(formation=formation_obj.id)
            qualification = formation_obj.qualification
            branche = fiche.specialite.branche
            montant_specialite = fiche.specialite.prix

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

    documents = []
    for i in documents_qs:
        documents.append({'label' : i.label})

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
        'specialite': specialite_label,
        'annee_academique': annee_academique,
        'echeancier': echeancier,
        'documents' : documents,
        'formation' : formation_label,
        'groupe': current_groupe.nom if current_groupe else '',
        'date_entree': date_entree.isoformat() if date_entree else None,
        'date_sortie': date_sortie.isoformat() if date_sortie else None,
        'matricule' : student.matricule_interne,
        "qualification" : qualification,
        "branche" : branche,
        "date_debut" : current_groupe.start_date.isoformat() if current_groupe and current_groupe.start_date else '',
        "date_fin" : current_groupe.end_date.isoformat() if current_groupe and current_groupe.end_date else '',
        "montant_specialite" : float(montant_specialite) if montant_specialite else 0.0,
    }
    
    return context_data
