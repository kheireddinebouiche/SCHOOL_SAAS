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

    context = {
        'modules' : modules,
        'specialites' : specialite,
        'formateurs_json': json.dumps(list(formateurs))
    }
    return render(request, 'tenant_folder/formateur/affectation_modules.html', context)

@login_required(login_url="institut_app:login")
def LoadAssignedProf(request):
    if request.method == "GET":
        moduleId = request.GET.get('moduleId')
        if not moduleId:
            return JsonResponse({"status" : "error" , "messages" : "Erreur ! ID module indisponible"})
        
        liste = EnseignantModule.objects.filter(module_id = moduleId).values('id','formateur__nom','formateur__prenom')

        return JsonResponse(list(liste), safe=False)
    else:
        return JsonResponse({"status" : "error"})