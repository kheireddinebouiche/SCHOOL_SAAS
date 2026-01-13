from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from django.db.models import Q
from datetime import datetime
from ..models import *
from django.db import transaction
from django.utils.dateformat import format
from institut_app.decorators import *


@login_required(login_url='institut_app:login')
@module_permission_required('crm','view')
@module_permission_required('crm','add')
@module_permission_required('crm','approuv')
@role_required('crm', ['Administrateur','Superviseur'])
def liste_derogations(request):
   
    context = {
        'page_title': 'Liste des dérogations',

    }
    return render(request, 'tenant_folder/crm/liste_derogations.html', context)


@login_required(login_url='institut_app:login')
def LoadDerogations(request):
    liste = Derogations.objects.all().values('id','motif','date_de_demande','statut', 'type','demandeur','demandeur__nom','demandeur__prenom','updated_at')
    for i in liste:
        i_obj  = Derogations.objects.get(id = i['id'])
        i['updated_at'] = format(i_obj.updated_at, "Y-m-d H:i")
    return JsonResponse(list(liste), safe=False)

@login_required(login_url="institut_app:login")
def ApiCheckDerogationStatus(request):
    id_preinscrit = request.GET.get('id_preinscrit')
    try:
        obj = Derogations.objects.filter(demandeur__id = id_preinscrit, motif="Documents Incomplets").last()
        data = {
            'date_de_demande' : obj.date_de_demande,
            'date_de_traitement' : obj.date_de_traitement,
            'observation' : obj.observation,
            'motif' : "Documents Incomplets",
            'statut' : obj.get_statut_display(),
        }
        return JsonResponse({"status": obj.statut,'data':data}, safe=False)
    except:
        return JsonResponse({"status": "error"})
   
@login_required(login_url="institut_app:login")
def ApiStoreDerogation(request):
    id_preinscrit = request.POST.get('id_preinscrit')
    reason = request.POST.get('reason')

    preinscrit = Prospets.objects.get(id = id_preinscrit)
   
    Derogations.objects.create(
        demandeur = preinscrit,
        type = reason,
        motif = "Documents Incomplets",
        
    )

    return JsonResponse({"status" : 'success', 'message' : "La demande de dérogation est en attente de traitement."})

@login_required(login_url="institut_app:login")
def ApiGetDerogationDetails(request):
    id_derogation = request.GET.get('id_derogation')
    obj = Derogations.objects.get(id = id_derogation)

    data={
        'id' : obj.id,
        'demandeur' : obj.demandeur.id,
        'demandeur_nom' : obj.demandeur.nom,
        'demandeur_prenom' : obj.demandeur.prenom,
        'is_double' : obj.demandeur.is_double,
        'type' : obj.type,
        'motif' : obj.motif,
        'date_de_demande' : obj.date_de_demande,
        'statut' : obj.statut,
        'observation' : obj.observation,
    }

    return JsonResponse(data, safe=False)

@login_required(login_url="institut_app:login")
@transaction.atomic
def ApiTraiteDerogation(request):
    decision = request.POST.get('decision')
    commentaire = request.POST.get('commentaire')
    id_derogation = request.POST.get('id_derogation')

    obj = Derogations.objects.get(id = id_derogation)

    obj.etat = True
    obj.statut = decision
    obj.observation = commentaire

    obj.save()


    prospect = Prospets.objects.get(id = obj.demandeur.id)

    if decision == "acceptee":
        prospect.has_derogation = True
        prospect.save()
    else:
        prospect.has_derogation = False
        prospect.save()

    return JsonResponse({"status" : "success"})