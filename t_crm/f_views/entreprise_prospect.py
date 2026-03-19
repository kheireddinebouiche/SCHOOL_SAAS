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
        'observation',
        'rc', 'nif', 'nis', 'art_imp',
        'adresse', 'wilaya', 'code_zip',
        'motif_annulation').first()
    
    if prospect:
        obj = Prospets.objects.get(id= prospect['id'])
        prospect['created_at'] = prospect['created_at'].strftime("%Y-%m-%d %H:%M")
        prospect['statut_label'] = obj.get_statut_display()
        prospect['logo_entreprise_url'] = obj.logo_entreprise.url if obj.logo_entreprise else None

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
    prospect_obj.rc = request.POST.get('rc')
    prospect_obj.nif = request.POST.get('nif')
    prospect_obj.nis = request.POST.get('nis')
    prospect_obj.art_imp = request.POST.get('art_imp')
    prospect_obj.adresse = request.POST.get('adresse')
    prospect_obj.wilaya = request.POST.get('wilaya')
    prospect_obj.code_zip = request.POST.get('code_zip')

    if request.FILES.get('logo_entreprise'):
        prospect_obj.logo_entreprise = request.FILES.get('logo_entreprise')

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
