from django.shortcuts import render, redirect
from django.http import JsonResponse
from ..forms import *
from ..models import *
from institut_app.models import *
from django.contrib import messages
from django.db import transaction
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from t_groupe.models import *
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
import json
from t_etudiants.models import *
from t_formations.models import Formateurs, DoubleDiplomation, CorrepondanceModule


def checkFormateurDispo(formateur_id, jour, heure_debut, heure_fin):
    """
    Vérifie si le formateur est déjà occupé pendant cette plage horaire.
    Retourne True si occupé, False si disponible.
    """
    return TimetableEntry.objects.filter(
        formateur_id=formateur_id,
        jour=jour,
        heure_debut__lt=heure_fin, 
        heure_fin__gt=heure_debut,
        timetable__status = "enc",
    ).exists()

def checkSalleDispo(salle , jour, heure_debut, heure_fin):
    """
    Vérifie si la est déjà occupé pendant cette plage horaire.
    Retourne True si occupé, False si disponible.
    """
    return TimetableEntry.objects.filter(
        salle_id=salle,
        jour=jour,
        heure_debut__lt=heure_fin, 
        heure_fin__gt=heure_debut,
        timetable__status = "enc"
    ).exists()

def checkFormateurDispoByStoredAvailability(formateur_id, jour, heure_debut, heure_fin):
    try:
        formateur = Formateurs.objects.get(id=formateur_id)

        if not formateur.dispo or 'disponibilites' not in formateur.dispo:
            return False, "Le formateur n'a aucune disponibilité enregistrée."

        disponibilites = formateur.dispo['disponibilites']

        # Récupérer toutes les plages du jour
        plages_du_jour = [
            d for d in disponibilites
            if d.get('jour', '').lower() == jour.lower()
        ]

        if not plages_du_jour:
            return False, f"Le formateur n'est pas disponible le {jour}."

        # Tester chaque plage
        for plage in plages_du_jour:
            dispo_debut = plage.get('heure_debut')
            dispo_fin = plage.get('heure_fin')

            if not dispo_debut or not dispo_fin:
                continue  # on ignore les plages mal formées

            # Comparaison (heures sous forme HH:MM)
            if heure_debut >= dispo_debut and heure_fin <= dispo_fin:
                return True, (
                    f"Disponible le {jour} de {dispo_debut} à {dispo_fin}"
                )

        # Si aucune plage ne correspond
        plages_txt = ", ".join(
            [f"{p.get('heure_debut')}–{p.get('heure_fin')}" for p in plages_du_jour]
        )

        return False, (
            f"Le formateur est disponible le {jour} uniquement sur les plages : {plages_txt}."
        )

    except Formateurs.DoesNotExist:
        return False, "Le formateur spécifié n'existe pas."
    except Exception as e:
        return False, f"Erreur lors de la vérification de la disponibilité : {str(e)}"

def CheckAssignedCours(timetable, teacher, cours):
    return TimetableEntry.objects.filter(
        timetable_id = timetable,
        formateur_id = teacher,
        cours__code = cours
    ).exists()

def PreventAffectModuleForOtherTeache(timetable, teacher, cours):
    """
    Vérifie si un module est déjà affecté à un autre formateur dans le même emploi du temps.
    Retourne True si le module est déjà attribué à un autre enseignant.
    """
    obj = TimetableEntry.objects.filter(
        timetable_id=timetable,
        cours__code=cours
    ).first()

    if not obj:
        return False  # Aucun cours trouvé → pas de conflit

    teacher_id = int(teacher)  # convertir le paramètre POST en entier

    # Si le module est déjà attribué à un autre formateur
    if obj.formateur and obj.formateur.id != teacher_id:
        return True

    return False

def checkAssignedSameHoraire(jour,heure_debut,heure_fin,timetable):
    return TimetableEntry.objects.filter(
        heure_debut = heure_debut,
        heure_fin = heure_fin,
        jour = jour,
        timetable_id = timetable,
    ).exists()

@login_required(login_url="institut_app:login")
@transaction.atomic
def save_session(request):

    session_module = request.POST.get('session_module')
    session_professeur = request.POST.get('session_professeur')
    session_jour = request.POST.get('session_jour')
    heure_debut = request.POST.get('heure_debut')
    heure_fin = request.POST.get('heure_fin')
    session_salle = request.POST.get('session_salle')
    timetable_id = request.POST.get('pk')
    
    # Récupérer l'objet Timetable
    timetable = get_object_or_404(Timetable, id=timetable_id)
    current_specialite = timetable.groupe.specialite
    
    # --- LOGIQUE DOUBLE DIPLOMATION ---
    is_shared_session = False
    partner_specialite = None
    
    # 1. Vérifier si cette spécialité est dans une DoubleDiplomation
    double_diplomation = DoubleDiplomation.objects.filter(
        Q(specialite1=current_specialite) | Q(specialite2=current_specialite)
    ).first()
    
    if double_diplomation:
        # 2. Identifier la spécialité partenaire
        if double_diplomation.specialite1 == current_specialite:
            partner_specialite = double_diplomation.specialite2
        else:
            partner_specialite = double_diplomation.specialite1
            
        # 3. Vérifier si module est dans CorrepondanceModule pour cette DD
        # On compare par code du module
        is_shared_module = CorrepondanceModule.objects.filter(
            formation=double_diplomation,
            modules__code=session_module
        ).exists()
        
        if is_shared_module:
            is_shared_session = True

    # --- VERIFICATIONS DISPONIBILITE ---

    # A. Formateur
    # On récupère tous les conflits potentiels (hors timetable courant, supposons que le formateur ne peut pas être à 2 endroits)
    # Note: checkFormateurDispo ci-dessus fait une vérif simple. Ici on fait une vérif détaillée.
    
    teacher_conflicts = TimetableEntry.objects.filter(
        formateur_id=session_professeur,
        jour=session_jour,
        heure_debut__lt=heure_fin, 
        heure_fin__gt=heure_debut,
        timetable__status="enc"
    )
    # Exclure l'emploi du temps courant si on veut (mais ici save_session = ajout, pas modif ?)
    # Si c'est un ajout, on ne devrait pas avoir de conflit avec soi-même sauf si on ajoute 2 fois.
    
    for conflict in teacher_conflicts:
        # Si c'est un conflit standard (pas partagé), on bloque
        is_valid_conflict = False
        
        if is_shared_session and partner_specialite:
            # Le conflit est accepté SI :
            # - C'est le MEME module
            # - C'est la spécialité PARTENAIRE
            # - (Optionnel) C'est le même semestre, vérifié implicitement par "le même module" souvent
            if partner_specialite:
                # Vérifier si c'est un module équivalent
                # On réutilise la logique de correspondence si possible, ou on vérifie si le module du conflit est dans correspondance
                 is_equivalent = CorrepondanceModule.objects.filter(
                    formation=double_diplomation,
                    modules=conflict.cours 
                 ).exists() and CorrepondanceModule.objects.filter(
                    formation=double_diplomation,
                    modules__code=session_module
                 ).exists()

                 # Simplification: est-ce que le module en conflit fait partie de la MEME correspondance que le module session ?
                 # On a déjà trouvé "is_shared_module" qui valide que "session_module" est shared.
                 # Maintenant on vérifie que "conflict.cours" est aussi dans cette correspondance.
                 
                 if is_equivalent and conflict.timetable.groupe.specialite == partner_specialite:
                    is_valid_conflict = True
        
        if not is_valid_conflict:
             # Si ce n'est pas un conflit "validé" par la double diplomation, c'est un vrai conflit
            return JsonResponse({"status": "error", "message": "Le formateur est déjà pris sur cette plage horaire."})


    # B. Salle
    room_conflicts = TimetableEntry.objects.filter(
        salle_id=session_salle,
        jour=session_jour,
        heure_debut__lt=heure_fin, 
        heure_fin__gt=heure_debut,
        timetable__status="enc"
    )
    
    for conflict in room_conflicts:
         is_valid_conflict = False
         
         if is_shared_session and partner_specialite:
             is_equivalent = CorrepondanceModule.objects.filter(
                formation=double_diplomation,
                modules=conflict.cours 
             ).exists() and CorrepondanceModule.objects.filter(
                formation=double_diplomation,
                modules__code=session_module
             ).exists()

             if is_equivalent and conflict.timetable.groupe.specialite == partner_specialite:
                 is_valid_conflict = True
                 
         if not is_valid_conflict:
             return JsonResponse({"status": "error", "message": "La salle est déjà prise sur cette plage horaire."})


    # C. Disponibilité déclarée (horaires de travail)
    is_available, availability_message = checkFormateurDispoByStoredAvailability(session_professeur, session_jour, heure_debut, heure_fin)
    if not is_available:
        return JsonResponse({"status": "error", "message": availability_message})

    
    # D. Autres vérifications métier
    if PreventAffectModuleForOtherTeache(timetable_id, session_professeur, session_module):
        return JsonResponse({"status": "error", "message": "Le module a été déja affecter a un autre formateur"})
    
    if checkAssignedSameHoraire(session_jour,heure_debut,heure_fin,timetable_id):
        return JsonResponse({"status":"error","message": "Une séance est déjà programmée pour le même créneau horaire"})
    
    # Création
    TimetableEntry.objects.create(
        timetable_id = timetable_id,
        cours= Modules.objects.get(code=session_module),
        salle_id= session_salle,
        formateur_id= session_professeur,
        jour = session_jour,
        heure_debut = heure_debut,
        heure_fin = heure_fin
    )

    return JsonResponse({"status" : "success", "message" : "Cours plannifier avec succès"})


### FONCTION PERMETANT DE CONFIGURER LES LIGNES DE LEMPLOIE DU TEMPS ###
@login_required(login_url="institut_app:login")
def timetable_edit(request, pk):
    timetable = Timetable.objects.get(id = pk)

    creneau_data = timetable.creneau.jour_data
    creneau_horaire = timetable.creneau.horaire_data

    modules = ProgrammeFormation.objects.filter(specialite = timetable.groupe.specialite, semestre = timetable.semestre)
    sales = Salle.objects.all()

    historique = TimetableEntry.objects.filter(timetable = timetable)

    context = {
        'timetable' : timetable,
        'jour_data' : creneau_data,
        'horaire_data' : creneau_horaire,
        'modules' : modules,
        'salles' : sales,
        'pk' : pk,
        'historique' : historique,
    }
    if timetable.is_configured:
        return render(request, 'tenant_folder/timetable/configure_timetable_cours.html', context)
    else:
        return render(request, 'tenant_folder/timetable/configuration_emploie.html', context)

@login_required(login_url="institut_app:login")
def ApiLoadTableEntry(request):
    timetable_id = request.GET.get('timetable')
    mode = request.GET.get('mode') # 'normal' or 'double_degree'

    timetable = get_object_or_404(Timetable, id=timetable_id)
    
    # 1. Base History (Current Timetable)
    historique = list(TimetableEntry.objects.filter(timetable=timetable).values(
        'id', 'cours__label', 'cours__code', 'heure_debut', 'heure_fin', 
        'jour', 'formateur__nom', 'formateur__prenom', 'salle__nom', 
        'salle__code', 'timetable__is_validated'
    ))

    # 2. If Double Degree Mode, fetch matching sessions from partner
    if mode == 'double_degree':
        current_specialite = timetable.groupe.specialite
        dd = DoubleDiplomation.objects.filter(Q(specialite1=current_specialite) | Q(specialite2=current_specialite)).first()
        
        if dd:
            partner_spec = dd.specialite2 if dd.specialite1 == current_specialite else dd.specialite1
            
            # Find Correspondence Modules
            correspondences = CorrepondanceModule.objects.filter(formation=dd).prefetch_related('modules')
            
            # Map module code -> Correspondence Label
            shared_module_map = {}
            for corr in correspondences:
                 for m in corr.modules.all():
                     shared_module_map[m.code] = corr.label

            shared_module_codes = list(shared_module_map.keys())

            # Find Partner Sessions
            # We look for sessions in timetables of the partner speciality, for these modules
            partner_sessions = TimetableEntry.objects.filter(
                timetable__groupe__specialite=partner_spec,
                cours__code__in=shared_module_codes,
                timetable__status__in=['enc', 'val', 'ter'] # Active timetables
            ).exclude(timetable__id=timetable_id) # Should not happen if different speciality but good practice
            
            if timetable.annee_scolaire:
                 partner_sessions = partner_sessions.filter(timetable__annee_scolaire=timetable.annee_scolaire)

            # Filter by Student Overlap (Critical)
            # Only include sessions from groups that actually share students
            my_student_ids = set(GroupeLine.objects.filter(groupe=timetable.groupe).values_list('student_id', flat=True))
            
            valid_partner_sessions = []
            checked_partner_groups = {} # Cache for group check

            for sess in partner_sessions:
                p_group_id = sess.timetable.groupe.id
                
                if p_group_id not in checked_partner_groups:
                    p_student_ids = set(GroupeLine.objects.filter(groupe_id=p_group_id).values_list('student_id', flat=True))
                    # Check overlap
                    checked_partner_groups[p_group_id] = bool(my_student_ids.intersection(p_student_ids))
                
                if checked_partner_groups[p_group_id]:
                    # Use Correspondence Label if available
                    module_label = shared_module_map.get(sess.cours.code, sess.cours.label)
                    
                    # Add to list with formatted structure
                    valid_partner_sessions.append({
                        'id': sess.id,
                        'cours__label': f"{module_label} (Double Diplôme)", # Mark it
                        'cours__code': sess.cours.code,
                        'heure_debut': sess.heure_debut,
                        'heure_fin': sess.heure_fin,
                        'jour': sess.jour,
                        'formateur__nom': sess.formateur.nom if sess.formateur else 'N/A',
                        'formateur__prenom': sess.formateur.prenom if sess.formateur else '',
                        'salle__nom': sess.salle.nom if sess.salle else 'N/A',
                        'salle__code': sess.salle.code if sess.salle else '',
                        'timetable__is_validated': sess.timetable.is_validated,
                        'is_shared': True # Flag identifying it's external
                    })
            
            # Merge
            historique.extend(valid_partner_sessions)

    # Custom sorting or processing
    for entry in historique:
        if entry['heure_debut']:
            entry['heure_debut'] = str(entry['heure_debut'])[:5]
        if entry['heure_fin']:
            entry['heure_fin'] = str(entry['heure_fin'])[:5]
            
    return JsonResponse(historique, safe=False)

@login_required(login_url="institut_app:login")
def ApiLoadTeacherGlobalTimetable(request):
    """
    Fetches all active sessions for a specific teacher across all timetables.
    """
    teacher_id = request.GET.get('teacher_id')
    formateur = get_object_or_404(Formateurs, id=teacher_id)
    
    # Fetch active sessions
    sessions = TimetableEntry.objects.filter(
        formateur=formateur,
        timetable__status__in=['enc', 'val'] # Active timetables
    ).values(
        'id', 'cours__label', 'cours__code', 'heure_debut', 'heure_fin', 
        'jour', 'formateur__nom', 'formateur__prenom', 'salle__nom', 
        'salle__code', 'timetable__is_validated', 'timetable__groupe__nom'
    )
    
    formatted_sessions = list(sessions)
    
    # Process time format and append Group info to module label for context
    for entry in formatted_sessions:
        if entry['heure_debut']:
            entry['heure_debut'] = str(entry['heure_debut'])[:5]
        if entry['heure_fin']:
            entry['heure_fin'] = str(entry['heure_fin'])[:5]
        
        # Append group name to context (since we are aggregating from multiple groups)
        if entry['timetable__groupe__nom']:
            entry['cours__label'] = f"{entry['cours__label']} ({entry['timetable__groupe__nom']})"

    return JsonResponse(formatted_sessions, safe=False)

@login_required(login_url="institut_app:login")
def ApiCheckSharedSession(request):
    timetable_id = request.GET.get('timetable_id')
    module_code = request.GET.get('module_code')
    
    if not all([timetable_id, module_code]):
        return JsonResponse({"found": False})

    timetable = get_object_or_404(Timetable, id=timetable_id)
    current_specialite = timetable.groupe.specialite
    
    # 1. Chercher les correspondances contenant ce module
    correspondences = CorrepondanceModule.objects.filter(modules__code=module_code).select_related('formation').prefetch_related('modules')
    
    for corr in correspondences:
        dd = corr.formation
        if not dd:
            continue
            
        # 2. Vérifier si ma spécialité fait partie de cette Double Diplomation
        partner_specialite = None
        if dd.specialite1 == current_specialite:
            partner_specialite = dd.specialite2
        elif dd.specialite2 == current_specialite:
            partner_specialite = dd.specialite1
            
        if partner_specialite:
            # Récupérer TOUS les modules équivalents dans cette correspondance
            equivalent_modules = corr.modules.all()
            equivalent_codes = [m.code for m in equivalent_modules]

            # 3. Chercher SI la spécialité partenaire a déjà programmé UN de ces modules
            query = TimetableEntry.objects.filter(
                timetable__groupe__specialite=partner_specialite,
                cours__code__in=equivalent_codes
            ).exclude(timetable__id=timetable_id)
            
            if timetable.annee_scolaire:
                query = query.filter(timetable__annee_scolaire=timetable.annee_scolaire)
            
            # On récupère tous les candidats potentiels (pas juste le premier) pour vérifier les étudiants
            candidate_sessions = query.select_related('timetable', 'salle', 'formateur', 'timetable__groupe', 'cours').order_by('-timetable__date_modification')
            
            # Récupérer les ID des étudiants du groupe ACTUEL
            current_group_students_ids = set(GroupeLine.objects.filter(groupe=timetable.groupe).values_list('student_id', flat=True))

            for existing_session in candidate_sessions:
                # Vérification : Est-ce que le groupe partenaire partage des étudiants avec nous ?
                partner_group = existing_session.timetable.groupe
                partner_group_students_ids = set(GroupeLine.objects.filter(groupe=partner_group).values_list('student_id', flat=True))
                
                # Intersection : s'il y a au moins un étudiant en commun
                if current_group_students_ids.intersection(partner_group_students_ids):
                    return JsonResponse({
                        "found": True,
                        "day": existing_session.jour,
                        "start_time": existing_session.heure_debut.strftime("%H:%M"),
                        "end_time": existing_session.heure_fin.strftime("%H:%M"),
                        "room": f"{existing_session.salle.nom} ({existing_session.salle.code})",
                        "group": existing_session.timetable.groupe.nom,
                        "teacher": f"{existing_session.formateur.nom} {existing_session.formateur.prenom}",
                        "teacher_id": existing_session.formateur.id,
                        "teacher_id": existing_session.formateur.id,
                        "module_matched": f"{existing_session.cours.label} ({existing_session.cours.code})",
                        "salle_id": existing_session.salle.id
                    })
    
    return JsonResponse({"found": False})