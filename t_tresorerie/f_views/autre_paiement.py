from django.shortcuts import render
from django.http import JsonResponse
from ..models import *
from django.db import transaction
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
import json
from t_crm.models import RemiseAppliquer, Prospets,FicheDeVoeux, FicheVoeuxDouble
from django.db.models import Q, Sum, F, Case, When, Value, CharField, Count



@login_required(login_url="institut_app:login")
def PageAutresPaiement(request):
    return render(request,'tenant_folder/comptabilite/paiements/liste_autres_paiement.html')


@login_required(login_url="institut_app:login")
def PageNouveauAutrePaiement(request):
    return render(request, 'tenant_folder/comptabilite/paiements/nouveau_autre_paiement.html')

@login_required(login_url="institut_app:login")
def ApiListeAutresPaiements(request):
    if request.method == "GET":
        pass

    else:
        return JsonResponse({"status":"error"})