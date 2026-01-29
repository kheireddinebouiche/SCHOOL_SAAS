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
    entites = Entreprise.objects.all()
    return render(request, 'tenant_folder/comptabilite/paiements/nouveau_autre_paiement.html',{'entites': entites})

@login_required(login_url="institut_app:login")
def ApiListeAutresPaiements(request):
    if request.method == "GET":
        entite_id = request.GET.get('entite_id')
        paiements = AutreProduit.objects.all().select_related('client', 'compte').order_by('-date_paiement')
        
        if entite_id:
            paiements = paiements.filter(entite_id=entite_id)
            
        data = []

        for p in paiements:
            data.append({
                'id': p.id,
                'prospect_nom': p.client.nom if p.client else "Anonyme",
                'prospect_prenom': p.client.prenom if p.client and p.client.prenom else "",
                'description': p.label,
                'num': p.num if p.num else f"AUT-{p.id}",  # Use p.num here!
                'montant_paye': float(p.montant_paiement) if p.montant_paiement else 0,
                'context': p.compte.name if p.compte else "Autre",
                'context_key': 'autre',
                'mode_paiement': p.get_mode_paiement_display(),
                'date_operation': p.date_operation.strftime('%Y-%m-%d') if p.date_operation else "-",
                'date_paiement': p.date_paiement.strftime('%Y-%m-%d') if p.date_paiement else "-"
            })

        return JsonResponse(data, safe=False)

    else:
        return JsonResponse({"status":"error"})