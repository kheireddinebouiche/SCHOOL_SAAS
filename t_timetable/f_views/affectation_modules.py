from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from ..forms import *
from ..models import *
from institut_app.models import *
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required
from t_groupe.models import *
from django.views.decorators.http import require_http_methods
from django.db.models import Count
import json

@login_required(login_url="institut_app:login")
def PageAffectation(request):

    modules = Modules.objects.annotate(nombre_formateur = Count('affect_module'))
    specialite = Specialites.objects.all()
    formateurs = Formateurs.objects.all().values('id', 'nom', 'prenom', 'email')

    affectations = EnseignantModule.objects.values('formateur_id', 'module_id')
    affectations_list = list(affectations)

    context = {
        'modules' : modules,
        'specialites' : specialite,
        'formateurs_json': json.dumps(list(formateurs)),
        'affectations_json': json.dumps(affectations_list),
    }
    return render(request, 'tenant_folder/formateur/affectation_modules.html', context)

@login_required(login_url="institut_app:login")
def ApiLoadModules(request):
    modules = Modules.objects.annotate(nombre_formateur = Count('affect_module')).values('id','label','code','specialite__label', 'nombre_formateur')

    return JsonResponse(list(modules), safe=False)


@login_required(login_url="institut_app:login")
def LoadAssignedProf(request):
    if request.method == "GET":
        moduleId = request.GET.get('moduleId')
        if not moduleId:
            return JsonResponse({"status" : "error" , "messages" : "Erreur ! ID module indisponible"})
        
        liste = EnseignantModule.objects.filter(module_id = moduleId).values('id','formateur__nom','formateur__prenom','formateur__email')

        return JsonResponse(list(liste), safe=False)
    else:
        return JsonResponse({"status" : "error"})
    
@login_required(login_url="insitut_app:login")
@transaction.atomic
def ApiAffectTrainer(request):
    if request.method == "POST":
        trainerId = request.POST.get('trainerId')
        moduleId = request.POST.get('moduleId')

        if not trainerId and not moduleId:
            return JsonResponse({"status" : "error", "message" : "Des données sont manquante lors du traitement de la requete"})
        
        EnseignantModule.objects.create(
            module_id=moduleId,
            formateur_id = trainerId
        )
        return JsonResponse({"status" : "success", "message" : "L'enseignant à été affecter avec succès"})
    else:
        return JsonResponse({"status" : "error", "message" : "Methode non autoriser"})