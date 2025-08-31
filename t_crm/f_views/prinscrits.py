from django.shortcuts import render,redirect
from django.http import JsonResponse
from ..models import *
from ..forms import *
from django.contrib import messages
from t_tresorerie.models import *
from t_formations.models import *
from django.db import transaction
from django.db.models import Count, Q
from django.core.exceptions import PermissionDenied
from functools import wraps
from decimal import Decimal
from django.contrib.auth.decorators import login_required


@login_required(login_url='intitut_app:login')
def ListeDesPrinscrits(request):
    context = {
        'tenant' : request.tenant
    }

    return render(request,'tenant_folder/crm/preinscrits/liste-des-preinscrits.html', context)

@login_required(login_url='institut_app:login')
def ApiLoadPrinscrits(request):
    liste = Prospets.objects.filter(statut = "prinscrit").values('id', 'nin', 'nom', 'prenom', 'type_prospect','email','telephone','canal','created_at','etat','entreprise')
    for i in liste:
        i_obj = Prospets.objects.get(id=i['id'])
        i['etat_label'] = i_obj.get_etat_display()
        i['type_prospect_label'] = i_obj.get_type_prospect_display()
    return JsonResponse(list(liste), safe=False)

@login_required(login_url='intitut_app:login')
def DetailsPrinscrit(request, pk):
    
    context = {
        'pk' : pk,
        'tenant' : request.tenant
    }
    return render(request, 'tenant_folder/crm/preinscrits/details-preinscrit.html', context)

@login_required(login_url='institut_app:login')
def ApiLoadPreinscrisPerosnalInfos(request):
    id_prospect = request.GET.get('id_prospect')
    prospect = Prospets.objects.filter(id=id_prospect).values('created_at','id','nin','nom','prenom','email','telephone','type_prospect','canal','statut','etat','entreprise','poste_dans_entreprise','observation').first()
    
    return JsonResponse(prospect, safe=False)

@login_required(login_url='institut_app:login')
def ApiLoadPreinscritRendezVous(request):
   id_prospect = request.GET.get('id_prospect')
   rendez_vous = RendezVous.objects.filter(prospect__id=id_prospect, context="prinscrit").values('id','date_rendez_vous','heure_rendez_vous','type','object','created_at','statut')
   for l in rendez_vous:
       l_obj = RendezVous.objects.get(id = l['id'])
       l['status_label'] = l_obj.get_statut_display()
       l['type_label'] = l_obj.get_type_display()
       l['created_at'] = l_obj.created_at
   return JsonResponse(list(rendez_vous), safe=False)


@login_required(login_url='institut_app:login')
def ApiLoadNotePr(request):
    prospect_id = request.GET.get('id_prospect')
    notes = NotesProcpects.objects.filter(prospect__id = prospect_id, context="prinscrit").values('id','prospect','created_by__username','created_at','note','tage')
    for l in notes:
        l_obj = NotesProcpects.objects.get(id = l['id'])
        l['tage'] = l_obj.get_tage_display()
    return JsonResponse(list(notes), safe=False)


@login_required(login_url='intitut_app:login')
def ApiCheckHasCompletedProfile(request):
    id_preinscrit = request.GET.get('id_preinscrit')
    pass

@login_required(login_url='institut_app:login')
def ApiCheckCompletedDoc(request):
    id_preinscrit = request.GET.get('id_preinscrit')
    statut = Prospets.objects.get(id = id_preinscrit)

    data = {
        'has_completed_doc': str(statut.has_completed_doc).lower(),
    }
    return JsonResponse(data)

@login_required(login_url='intitut_app:login')
def ApiUpdatePreinscritInfos(request):
    pass