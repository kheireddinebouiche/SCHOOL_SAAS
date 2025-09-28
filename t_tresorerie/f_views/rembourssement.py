from django.shortcuts import render
from django.http import JsonResponse
from ..models import *
from django.db import transaction
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
import json
from t_crm.models import RemiseAppliquer, Prospets, FicheDeVoeux
from django.db.models import Q, Sum, F, Case, When, Value, CharField, Count
from institut_app.decorators import *
from t_crm.models import *
from datetime import datetime
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from t_tresorerie.models import *


def listeDesRembourssement(request):
    return render(request, "tenant_folder/comptabilite/tresorerie/liste-des-rembourssement.html")


@login_required
@require_http_methods(["GET"])
def ApiLoadRemboursements(request):
    
    clients = Prospets.objects.filter(
        statut="annuler", type_prospect="particulier"
    ).values("id", "nom", "prenom")

    rembourssement_data = []

    for client in clients:
        remboursements = Rembourssements.objects.filter(client=client['id']).values(
            'id', 'allowed_amount'
        )
        
        rembourssement_data.append({
            'client': client,
            'remboursements': list(remboursements)
        })

    return JsonResponse(rembourssement_data, safe=False)
