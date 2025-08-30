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