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


@login_required(login_url="institut_app:login")
def timetable_view(request):
    pass

### FONCTION PERMETANT DE CONFIGURER LES LIGNES DE LEMPLOIE DU TEMPS ###
@login_required(login_url="institut_app:login")
def timetable_edit(request, pk):
    timetable = Timetable.objects.get(id = pk)
    creneau_data = timetable.creneau.jour_data
    creneau_horaire = timetable.creneau.horaire_data

    modules = ProgrammeFormation.objects.filter(specialite = timetable.groupe.specialite, semestre = timetable.semestre)
    sales = Salle.objects.all()

    context = {
        'timetable' : timetable,
        'jour_data' : creneau_data,
        'horaire_data' : creneau_horaire,
        'modules' : modules,
        'salles' : sales
    }
    if timetable.is_configured:
        return render(request, 'tenant_folder/timetable/configure_timetable_cours.html', context)
    else:
        return render(request, 'tenant_folder/timetable/configuration_emploie.html', context)

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


@login_required(login_url="institut_app:login")
@transaction.atomic
def save_session(request):
    session_module = request.POST.get('session_module')
    session_professeur = request.POST.get('session_professeur')
    session_jour = request.POST.get('session_jour')
    session_horaire = request.POST.get('session_horaire')
    session_salle = request.POST.get('session_salle')

    pass