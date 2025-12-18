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
from t_etudiants.models import *
from t_formations.models import Formateurs

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
        extraordinary_timetable = request.POST.get('extraordinary_timetable')

        if extraordinary_timetable == False:
            try:
                obj = Timetable.objects.get(groupe_id=groupe, semestre=semestre)
                if obj:
                    return JsonResponse({"status":"error",'message' : "Emploie du temps déja crée pour le groupe pour le meme semestre"})
            except:
                pass
        else:
            find = Timetable.objects.filter(groupe_id=groupe, semestre = semestre, status="enc")
            timetable_list = ", ".join([str(f.label) for f in find])
            if find.exists():
                return JsonResponse({"status" : "error",'message' : f"Veuillez d'abord mettre en pause l'emploi du temps : {timetable_list}"})

        if Timetable.objects.filter(groupe_id = groupe, status="enc").exists():
            return JsonResponse({"status":"error","message":"Veuillez d'abord cloturer l'ancienne emploie du temps"})

        promo = Groupe.objects.get(id = groupe)

        Timetable.objects.create(
            label = label,
            groupe_id = groupe,
            semestre = semestre,
            description = description,
            annee_scolaire = promo.promotion.annee_academique,
        )
        messages.success(request,"L'emploie du temps à été crée avec succès")
        return JsonResponse({"status" : "success"})
    else:
        return JsonResponse({"status" : "error",'message' : "Methode non autoriser"})

@login_required(login_url="institut_app:login")
@transaction.atomic
def ApiDeleteTimeTable(request):
    if request.method == 'GET':
        id = request.GET.get('id')

        if not id:
            return JsonResponse({"status": "error","message":"Informations manquantes"})
        
        obj = Timetable.objects.get(id = id)

        if obj.is_validated:
            return JsonResponse({"status":"error","message" : "L'emploie du temps ne peux pas être supprimer."})
        
        obj.delete()
        messages.success(request, "L'emploie du temps à été supprimer avec succès")
        return JsonResponse({"status": "success","message":"L'emploie du temps à été supprimer avec succès"})
    else:
        return JsonResponse({'status':'error'})

@login_required(login_url="institut_app:login")
def timetable_view(request, pk):
    timetable = Timetable.objects.get(id = pk)
    sessions = timetable.entries.all()  # Using the related name
    
    # Get unique days from sessions and sort them
    days_set = set()
    for session in sessions:
        if session.jour:
            days_set.add(session.jour.lower())
    
    # Define day names mapping
    day_names = {
        'lundi': 'Lundi', 
        'mardi': 'Mardi', 
        'mercredi': 'Mercredi', 
        'jeudi': 'Jeudi', 
        'vendredi': 'Vendredi', 
        'samedi': 'Samedi', 
        'dimanche': 'Dimanche',
        'monday': 'Lundi',
        'tuesday': 'Mardi', 
        'wednesday': 'Mercredi', 
        'thursday': 'Jeudi', 
        'friday': 'Vendredi', 
        'saturday': 'Samedi', 
        'sunday': 'Dimanche',
    }
    
    # Define time slots based on actual sessions
    time_slots_set = set()
    for session in sessions:
        if session.heure_debut and session.heure_fin:
            time_slot = f"{session.heure_debut.strftime('%H:%M')} - {session.heure_fin.strftime('%H:%M')}"
            time_slots_set.add(time_slot)
    
    # Sort the time slots chronologically
    sorted_time_slots = sorted(list(time_slots_set))
    
    # Sort the days in a logical order (Monday to Sunday or based on first occurrence)
    # For this simple case, we'll sort alphabetically but could improve to order by week days
    sorted_days = sorted(list(days_set))
    
    context = {
        'timetable': timetable,
        'sessions': sessions,
        'day_names': day_names,
        'unique_days': sorted_days,
        'time_slots': sorted_time_slots,
    }
    return render(request, 'tenant_folder/timetable/details_timetable.html', context)

@login_required(login_url="institut_app:login")
@transaction.atomic
def ApiPausetimeTable(request):
    if request.method == "GET":
        id = request.GET.get('id')

        if not id:
            return JsonResponse({"status" : "error"})
        
        obj = Timetable.objects.get(id = id)
        obj.status = "pau"
        obj.save()
        return JsonResponse({"status":"success"})
    else:
        return JsonResponse({"status" : "error"})

@login_required(login_url="institut_app:login")
@transaction.atomic
def ApiClotureTimeTable(request):
    if request.method == "GET":
        id = request.GET.get('id')

        if not id:
            return JsonResponse({"status" : "error"})
        
        obj = Timetable.objects.get(id = id)
        obj.status = "ter"
        obj.save()
        return JsonResponse({"status":"success"})
    else:
        return JsonResponse({"status" : "error"})


def CheckIfExistsEncTimetable(groupe,semestre):
    return Timetable.objects.filter(
        status = "enc",
        groupe_id = groupe,
        semestre = semestre
    ).exists()

@login_required(login_url="institut_app:login")
@transaction.atomic
def ApiActivateTimeTable(request):
    if request.method == "GET":
        id = request.GET.get('id')
        if not id:
            return JsonResponse({"status" : "error"})
        obj = Timetable.objects.get(id = id)

        if CheckIfExistsEncTimetable(obj.groupe.id, obj.semestre):
            return JsonResponse({"status" : "error",'message' : "Une emploie du temps en cours est déja présente"})

        obj.status = "enc"
        obj.save()

        return JsonResponse({"status":"success"})
    else:
        return JsonResponse({"status" : "error"})


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


@login_required(login_url="institut_app:login")
@transaction.atomic
def ApiDeleteCoursSession(request):
    if request.method == "POST":
        cours = request.POST.get('id')
        if not cours:
            return JsonResponse({"status":"error",'message':"Informations manquantes"})

        obj = TimetableEntry.objects.get(id = cours)
        obj.delete()
        return JsonResponse({'status':"success",'message':"suppréssion effectuer avec succès"})
    else:
        return JsonResponse({"status":"error","message":"Méthode non autoriser."})

### FONCTION PERMETANT DE CONFIGURER LE MODELE DE CRENEAU ###
@login_required(login_url="institut_app:login")
def timetable_configure(request, pk):
    timetable = Timetable.objects.get(id = pk)
    crenau = ModelCrenau.objects.filter(is_active=True)
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
        crenau_model_id = request.GET.get('crenau_model_id')

        timetable = Timetable.objects.get(id = id_emploie)
        timetable.creneau_id = crenau_model_id
        timetable.is_configured=True
        timetable.save()
        return JsonResponse({"status" : "success","message" : "L'emploi du temps est desormais configurer"})
    else:
        messages.error(request, "Methode non autoriser")
        return JsonResponse({"status" : "error"})

@login_required(login_url="institut_app:login")
@transaction.atomic
def ApiValidateTimetable(request):
    id_emploie = request.GET.get('id_emploie')
    obj = Timetable.objects.get(id = id_emploie)
    obj.is_validated = True
    obj.save()

    messages.success(request, "Opération effectuer avec succès")
    return JsonResponse({"status" : "success"})


@login_required(login_url="institut_app:login")
@transaction.atomic
def ApiGenerateRegistre(request):
    if request.method == "POST":
        id = request.POST.get('id_emploie')
        obj = Timetable.objects.get(id = id)

        try:
            entries = TimetableEntry.objects.filter(timetable = obj)
            registre = CreateRegistre(obj.groupe.id,obj.semestre)

            for i in entries:
                CreateRegisterLine(i.cours.id, i.formateur.id,i.salle.nom,registre.id)
        except Exception as e:
            return JsonResponse({"status" : "error", "message" : str(e)})

    else:
        return JsonResponse({"status": "error", "message": "Méthode non autorisée"})


from django.db.models import Q


@transaction.atomic
def CreateRegistre(groupe,semestre):
    groupe_obj = Groupe.objects.get(id=groupe)
    registre, created = RegistrePresence.objects.update_or_create(
        label= groupe_obj,
        context="Génération automatique",
        defaults={
            'groupe_id': groupe,
            'semestre': semestre,
            'etat' : "enc",
            'annee_academique' : groupe_obj.promotion.annee_academique,
        }
    )
    return registre  # <-- retourne seulement l’objet, pas le tuple



@transaction.atomic
def CreateRegisterLine(module, teacher, salle, registre):
    ligne, created = LigneRegistrePresence.objects.update_or_create(
        module_id=module,
        teacher_id=teacher,
        room = salle,
        defaults={
            'type': "",
            'registre_id': registre
        }
    )
    return ligne
    

@login_required(login_url="insitut_app:login")
@transaction.atomic
def ApiMakeTimetableDraft(request):
    if request.method == "GET":
        id_emploie = request.GET.get('id_emploie')
        obj = Timetable.objects.get(id = id_emploie)
        obj.is_validated = False
        obj.save()
        messages.success(request,"L'emploie du temps est prêt pour etre modifier")
        return JsonResponse({"status" : "success"})
    else:
        return JsonResponse({"status" : "error",'message' : "Methode non autoriser"})

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

@login_required(login_url="insitut_app:login")
def get_formateur_dispo_status(request):
    formateur_id = request.GET.get('teacherId')
    formateur = Formateurs.objects.get(id=formateur_id)
    disponibilites = formateur.dispo.get("disponibilites", [])
    result = []

    for dispo in disponibilites:
        jour = dispo.get("jour")
        heure_debut = dispo.get("heure_debut")
        heure_fin = dispo.get("heure_fin")

        ## dispo du formateur
        h_debut = datetime.strptime(heure_debut, "%H:%M").time()
        h_fin = datetime.strptime(heure_fin, "%H:%M").time()

        ## calcule des heures non dispo
        taken_entries = TimetableEntry.objects.filter(
            formateur_id=formateur_id,
            jour=jour,
            heure_fin__gt=h_debut,
            heure_debut__lt=h_fin,
            timetable__status = "enc",
        ).order_by("heure_debut")

       
        libres = []
        current_start = h_debut

        for entry in taken_entries:
            if entry.heure_debut > current_start:
                libres.append({
                    "heure_debut": current_start.strftime("%H:%M"),
                    "heure_fin": entry.heure_debut.strftime("%H:%M")
                })
            current_start = max(current_start, entry.heure_fin)

        
        if current_start < h_fin:
            libres.append({
                "heure_debut": current_start.strftime("%H:%M"),
                "heure_fin": h_fin.strftime("%H:%M")
            })

        result.append({
            "jour": jour,
            "heure_debut": heure_debut,
            "heure_fin": heure_fin,
            "libre": libres
        })

    return JsonResponse({"result":result})

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


from django.db.models import Q

def get_salles_disponibles(jour, heure_debut, heure_fin):
    """
    Retourne les salles disponibles pour un jour et un créneau donné
    """

    # Salles occupées
    salles_occupees = TimetableEntry.objects.filter(
        jour=jour,
    ).exclude(
        timetable__status='ter'
    ).filter(
        Q(heure_debut__lt=heure_fin) &
        Q(heure_fin__gt=heure_debut)
    ).values_list('salle_id', flat=True)

    # Salles disponibles
    salles_disponibles = Salle.objects.exclude(
        id__in=salles_occupees
    )

    return salles_disponibles


from datetime import time

def salles_disponibles_view(request):
    
    heure_debut = request.GET.get('heur_debut')
    heure_fin = request.GET.get('heur_fin')
    jour = request.GET.get('jour')

    if not  heure_debut or not heure_fin or not jour:
        return JsonResponse({"status": "error", "message" : "Informations manquantes"})

    salles = get_salles_disponibles(jour, heure_debut, heure_fin)

    return JsonResponse({
        "salles": [
            {
                "id": salle.id,
                "nom": salle.nom,
                "code": salle.code,
                "capacite": salle.capacite,
                "type": salle.type_salle
            }
            for salle in salles
        ]
    })