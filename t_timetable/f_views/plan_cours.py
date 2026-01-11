from django.shortcuts import render, redirect
from django.http import JsonResponse
from ..forms import *
from ..models import *
from institut_app.models import *
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required
from t_groupe.models import *
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
import json
from t_etudiants.models import *
from t_formations.models import Formateurs



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
    timetable = request.POST.get('pk')


    if checkFormateurDispo(session_professeur, session_jour, heure_debut, heure_fin):
        return JsonResponse({"status": "error", "message": "Le formateur est déjà pris sur cette plage horaire."})

    is_available, availability_message = checkFormateurDispoByStoredAvailability(session_professeur, session_jour, heure_debut, heure_fin)
    if not is_available:
        return JsonResponse({"status": "error", "message": availability_message})

    if checkSalleDispo(session_salle, session_jour, heure_debut, heure_fin):
        return JsonResponse({"status": "error", "message": "La salle est déjà prise sur cette plage horaire."})
    
    if PreventAffectModuleForOtherTeache(timetable, session_professeur, session_module):
        return JsonResponse({"status": "error", "message": "Le module a été déja affecter a un autre formateur"})
    
    if checkAssignedSameHoraire(session_jour,heure_debut,heure_fin,timetable):
        return JsonResponse({"status":"error","message": "Une séance est déjà programmée pour le même créneau horaire"})
    
    TimetableEntry.objects.create(
        timetable_id = timetable,
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
    timetable=request.GET.get('timetable')
    historique = TimetableEntry.objects.filter(timetable = timetable).values('id','cours__label','cours__code','heure_debut','heure_fin','jour','formateur__nom','formateur__prenom','salle__nom','salle__code','timetable__is_validated')
    return JsonResponse(list(historique), safe=False)