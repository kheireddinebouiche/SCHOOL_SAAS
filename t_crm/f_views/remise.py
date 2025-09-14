from django.shortcuts import render,redirect
from django.http import JsonResponse
from ..models import *
from ..forms import *
from django.contrib import messages
from t_formations.models import *
from django.db import transaction
from django.db.models import Count, Q
from django.core.exceptions import PermissionDenied
from functools import wraps
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.utils.dateformat import format


@login_required(login_url="institut_app:login")
def ListeRemiseApplique(request):
    return render(request,"tenant_folder/crm/remises/liste_remise_appliquer.html")

@login_required(login_url="institut_app:login")
def AipLoadRemise(request):
    remises = Remises.objects.filter(is_enabled= True).values('id','label','taux','has_to_justify')
    return JsonResponse(list(remises), safe=False)

@login_required(login_url="institut_app:login")
def ApiLoadProspectParticulier(request):
    prospect = Prospets.objects.filter(type_prospect = 'particulier').values('id','nom','prenom','date_naissance','statut')

    for i in prospect:
        i_obj = Prospets.objects.get(id= i['id'])
        i['statut_label'] = i_obj.get_statut_display()

    return JsonResponse(list(prospect), safe=False)
 