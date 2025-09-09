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
from django.utils.dateformat import format


@login_required(login_url='institut_app:login')
def ApiLoadEntrepriseProspectInfo(request):
    id_prospect = request.GET.get('id_prospect')
    prospect = Prospets.objects.filter(id=id_prospect).values(
        'created_at','id','nin','nom','prenom','email',
        'telephone','type_prospect',
        'canal','statut','etat',
        'entreprise',
        'poste_dans_entreprise',
        'observation').first()
    
    if prospect:
        obj = Prospets.objects.get(id= prospect['id'])
        prospect['created_at'] = prospect['created_at'].strftime("%Y-%m-%d %H:%M")
        prospect['statut_label'] = obj.get_statut_display()   

    return JsonResponse(prospect, safe=False)

@login_required(login_url='institut_app:login')
@transaction.atomic
def ApiUpdateEntrepriseData(request):
    id_entreprise = request.POST.get('id_prospect')
    designation = request.POST.get('designation')
    observation = request.POST.get('observation')

    prospect_obj = Prospets.objects.get(id = id_entreprise)
    prospect_obj.entreprise = designation
    prospect_obj.observation = observation

    prospect_obj.save()

    return JsonResponse({"status" : "success"})

@login_required(login_url='institut_app:login')
@transaction.atomic
def ApiUpdateContactInfo(request):
    prenomUpdate = request.POST.get('prenomUpdate')
    emailUpdate = request.POST.get('emailUpdate')
    telephoneUpdate = request.POST.get('telephoneUpdate')
    nomUpdate = request.POST.get('nomUpdate')
    id_prospect = request.POST.get('id_prospect')

    prospect_obj = Prospets.objects.get(id = id_prospect)

    prospect_obj.nom = nomUpdate
    prospect_obj.prenom = prenomUpdate
    prospect_obj.telephone = telephoneUpdate
    prospect_obj.email = emailUpdate

    prospect_obj.save()

    return JsonResponse({"status" : "success"})
