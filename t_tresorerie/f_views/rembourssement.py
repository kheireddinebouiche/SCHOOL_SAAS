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
    
    clients = Prospets.objects.filter(statut="annuler", type_prospect="particulier").values("id", "nom", "prenom",'telephone','email')

    data = []

    for client in clients:
        remboursements = Rembourssements.objects.filter(client=client['id']).first()
        promotion = FicheDeVoeux.objects.filter(prospect = client['id'], is_confirmed=True).first()
        paiements = Paiements.objects.filter(prospect = client["id"], is_refund=False, context = "frais_f").aggregate(total=Sum('montant_paye'))['total'] or 0
        
        data.append({
            "client_id": client["id"],
            "nom": client["nom"],
            "prenom": client["prenom"],
            "telephone" : client["telephone"],
            "email" : client["email"],
            "remboursement_id": remboursements.id if remboursements else None,
            "allowed_amount": remboursements.allowed_amount if remboursements else None,
            "updated_at": remboursements.updated_at.strftime("%Y-%m-%d") if remboursements else None,
            "mode_rembourssement" : remboursements.get_mode_rembourssement_display() if remboursements else None,
            "motif_rembourssement" : remboursements.motif_rembourssement,
            "observation" : remboursements.observation,
            'promotion' : promotion.promo.code,
            'promotion_session' : promotion.promo.get_session_display(),
            'promotion_start' : promotion.promo.begin_year,
            'promotion_end' : promotion.promo.end_year,
            'specialite' : promotion.specialite.label,
            'total_paye' : paiements - remboursements.allowed_amount,
        })
        

    return JsonResponse(data, safe=False)
