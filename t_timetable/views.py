from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import *
from .models import *
from institut_app.models import *
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required
from t_groupe.models import *
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
import json

@login_required(login_url="institut_app:login")
def ListeDesSalles(request):
    salles = Salle.objects.all()
    context = {
        'salles' : salles
    }
    return render(request, 'tenant_folder/timetable/liste_des_salles.html', context)


@login_required(login_url="institut_app:login")
def ListeDesEmploie(request):
    liste = Timetable.objects.all()
    
    context = {
        'timetables' : liste
    }
    return render(request ,'tenant_folder/timetable/liste_des_emploies.html', context)

@login_required(login_url="institut_app:login")
def CreateTimeTable(request):
    groupes = Groupe.objects.all()
    context = {
        "groupes" : groupes,
    }
    return render(request, 'tenant_folder/timetable/ajouter_emploi_temps.html', context)

@login_required(login_url="insitut_app:login")
@transaction.atomic
def ApiCreateTimeTable(request):
    if request.method == "POST":
        label = request.POST.get('label')
        groupe = request.POST.get('groupe')
        semestre = request.POST.get('semestre')
        description = request.POST.get('description')
        print(label, groupe, semestre, description)
        Timetable.objects.create(
            label = label,
            groupe_id = groupe,
            semestre = semestre,
            description = description
        )
        return JsonResponse({"status" : "success",'message' : "L'emploie du temps à été crée avec succès"})
    else:
        return JsonResponse({"status" : "error",'message' : "Methode non autoriser"})


@login_required(login_url="institut_app:login")
def timetable_view(request, pk):
    timetable = Timetable.objects.get(id = pk)
    context = {
        'timetable' : timetable
    }
    return render(request, 'tenant_folder/timetable/details_timetable.html', context)

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
    historique = TimetableEntry.objects.filter(timetable = timetable).values('id','cours__label','cours__code','heure_debut','heure_fin','jour','formateur__nom','formateur__prenom','salle__nom','salle__code')
    return JsonResponse(list(historique), safe=False)



### FONCTION PERMETANT DE CONFIGURER LE MODELE DE CRENEAU ###
@login_required(login_url="institut_app:login")
def timetable_configure(request, pk):
    timetable = Timetable.objects.get(id = pk)
    crenau = ModelCrenau.objects.all()
    context = {
        'timetable' : timetable,
        'crenau' : crenau,
    }
    if timetable.is_configured:
        return render(request, 'tenant_folder/timetable/configure_timetable_cours.html', context)
    else:
        return render(request, 'tenant_folder/timetable/configuration_emploie.html', context)


@login_required(login_url="institut_app:login")
def FilterFormateur(request):
    if request.method == "GET":
        code_module = request.GET.get('code_module')
        if not code_module:
            return JsonResponse({"status" : "error",'message' : "Le code du module n'est pas disponible"})
        
        enseignants = EnseignantModule.objects.filter(module__code = code_module).values('id','formateur__id','formateur__nom','formateur__prenom')
        
        return JsonResponse(list(enseignants), safe=False)
    else:
        return JsonResponse({"status": "error",'message' : "Methode non autoriser"})

@login_required(login_url="institut_app:login")
@transaction.atomic
def ApiMakeTimetableDone(request):
    if request.method == "GET":
        id_emploie =  request.GET.get('id_emploie')
        crenau_model_id= request.GET.get('crenau_model_id')
        
        timetable = Timetable.objects.get(id = id_emploie)
        timetable.creneau_id = crenau_model_id
        timetable.is_configured=True
        timetable.save()
        return JsonResponse({"status" : "success","message" : "L'emploi du temps est desormais configurer"})
    else:
        messages.error(request, "Methode non autoriser")
        return JsonResponse({"status" : "error"})

def checkFormateurDispo(formateur_id, jour, heure_debut, heure_fin):
    """
    Vérifie si le formateur est déjà occupé pendant cette plage horaire.
    Retourne True si occupé, False si disponible.
    """
    return TimetableEntry.objects.filter(
        formateur_id=formateur_id,
        jour=jour,
        heure_debut__lt=heure_fin, 
        heure_fin__gt=heure_debut
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
        heure_fin__gt=heure_debut
    ).exists()

def checkFormateurDispoByStoredAvailability(formateur_id, jour, heure_debut, heure_fin):
    """
    Vérifie si le formateur est disponible selon ses disponibilités enregistrées dans le modèle Formateurs.
    Retourne (is_available, message) où is_available est True si disponible, False sinon.
    Le message contient des informations sur la disponibilité du formateur.
    """
    from t_formations.models import Formateurs
    try:
        formateur = Formateurs.objects.get(id=formateur_id)
        if not formateur.dispo or 'disponibilites' not in formateur.dispo:
            # Aucune disponibilité enregistrée, le formateur n'est pas disponible
            return False, f"Le formateur n'a aucune disponibilité enregistrée."
        
        disponibilites = formateur.dispo['disponibilites']
        
        # Vérifie si le jour demandé existe dans les disponibilités
        jour_dispo = None
        for dispo in disponibilites:
            if dispo.get('jour', '').lower() == jour.lower():
                jour_dispo = dispo
                break
        
        if not jour_dispo:
            # Le formateur n'est pas disponible ce jour-là
            return False, f"Le formateur n'est pas disponible le {jour}."
        
        # Compare les horaires
        dispo_heure_debut = jour_dispo.get('heure_debut')
        dispo_heure_fin = jour_dispo.get('heure_fin')
        
        if not dispo_heure_debut or not dispo_heure_fin:
            return False, f"Les heures de disponibilité du formateur sont incomplètes pour le {jour}."
        
        # Si les heures demandées sont en dehors de la plage disponible
        if heure_debut < dispo_heure_debut or heure_fin > dispo_heure_fin:
            return False, f"Le formateur est disponible le {jour} de {dispo_heure_debut} à {dispo_heure_fin}, mais la session demandée est de {heure_debut} à {heure_fin}."
        
        # Vérifie si la plage horaire demandée est incluse dans la plage disponible
        # Convertir les heures en format comparable (sous forme de chaînes pour comparaison)
        if heure_debut >= dispo_heure_debut and heure_fin <= dispo_heure_fin and heure_debut < heure_fin:
            return True, "Le formateur est disponible."
        else:
            return False, f"Le formateur est disponible le {jour} de {dispo_heure_debut} à {dispo_heure_fin}, mais la session demandée est de {heure_debut} à {heure_fin}."

    except Formateurs.DoesNotExist:
        # Le formateur n'existe pas
        return False, "Le formateur spécifié n'existe pas."
    except Exception as e:
        # En cas d'erreur, on considère que le formateur n'est pas disponible
        return False, f"Erreur lors de la vérification de la disponibilité: {str(e)}"

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

    # Vérifie disponibilité du formateur selon les emplois du temps existants
    if checkFormateurDispo(session_professeur, session_jour, heure_debut, heure_fin):
        return JsonResponse({"status": "error", "message": "Le formateur est déjà pris sur cette plage horaire."})

    # # Vérifie si le formateur est disponible selon ses disponibilités enregistrées
    # is_available, availability_message = checkFormateurDispoByStoredAvailability(session_professeur, session_jour, heure_debut, heure_fin)
    # if not is_available:
    #     return JsonResponse({"status": "error", "message": availability_message})

    if checkSalleDispo(session_salle, session_jour, heure_debut, heure_fin):
        return JsonResponse({"status": "error", "message": "La salle est déjà prise sur cette plage horaire."})
    
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