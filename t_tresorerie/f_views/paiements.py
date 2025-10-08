from django.shortcuts import render
from django.http import JsonResponse
from ..models import *
from django.db import transaction
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
import json
from t_crm.models import RemiseAppliquer, Prospets
from django.db.models import Q, Sum, F, Case, When, Value, CharField, Count


@login_required(login_url="institut_app:login")
def ListeDesPaiements(request):
    return render(request, 'tenant_folder/comptabilite/paiements/liste_des_paiements.html')

@login_required(login_url="institut_app:login")
def ApiListePaiements(request):
    liste = Paiements.objects.filter(is_refund=False)
    
    data= []
    for i in liste:
        data.append({
            'id' : i.id,
            'num' : i.num,
            'prospect_nom' : i.prospect.nom,
            'prospect_prenom' : i.prospect.prenom,
            'montant_paye' :i.montant_paye,
            'date_paiement':i.date_paiement,
            'mode_paiement' : i.get_mode_paiement_display(),
            'context' : i.get_context_display(),
            'context_key' : i.context
        })
        
    return JsonResponse(data, safe=False)
