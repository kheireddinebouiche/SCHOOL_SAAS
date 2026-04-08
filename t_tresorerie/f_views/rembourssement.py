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
from t_groupe.models import *
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
    
    # On récupère les IDs des clients ayant effectivement un enregistrement de remboursement
    refund_client_ids = Rembourssements.objects.values_list('client', flat=True)

    # On n'affiche que ceux qui ont un remboursement (peu importe leur statut d'annulation ou autre)
    clients = Prospets.objects.filter(
        id__in=refund_client_ids,
        type_prospect="particulier"
    ).values("id", "nom", "prenom",'telephone','email')

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
            "motif_rembourssement" : remboursements.motif_rembourssement if remboursements else None,
            "observation" : remboursements.observation if remboursements else None,
            'promotion' : promotion.promo.code if promotion and promotion.promo else None,
            'promotion_session' : promotion.promo.get_session_display() if promotion and promotion.promo else None,
            'promotion_start' : promotion.promo.begin_year if promotion and promotion.promo else None,
            'promotion_end' : promotion.promo.end_year if promotion and promotion.promo else None,
            'specialite' : promotion.specialite.label if promotion and promotion.specialite else None,
            'formation' : promotion.specialite.formation.nom if promotion and promotion.specialite and promotion.specialite.formation else None,
            'total_paye' : paiements - (remboursements.allowed_amount if remboursements and remboursements.allowed_amount else 0),
        })
        

    return JsonResponse(data, safe=False)


@login_required(login_url="institut_app:login")
def DetailsRembourssement(request, pk):
    obj = Rembourssements.objects.get(id = pk)
    voeux = FicheDeVoeux.objects.get(prospect = obj.client)
    total_paye = Paiements.objects.filter(prospect = obj.client, is_refund=False).aggregate(total=Sum('montant_paye'))['total'] or 0
    paiements = Paiements.objects.filter(prospect = obj.client)
    last_paiements = Paiements.objects.filter(prospect = obj.client, is_refund=False).last()

    groupe_line = GroupeLine.objects.filter(student = obj.client)

    entreprise = Entreprise.objects.get(id = voeux.specialite.formation.entite_legal.id)

    context = {
        'obj' : obj,
        'voeux' : voeux,
        'total_paye' : total_paye,
        'paiements' : paiements,
        'entreprise' : entreprise,
        'last_payment' : last_paiements,
        'groupe' : groupe_line,
    }
    return render(request, 'tenant_folder/comptabilite/rembourssement/details_rembourssement.html', context)

@login_required(login_url="institut_app:login")
def ApiLoadPaiements(request):
    if request.method == "GET":
        remboursement_id = request.GET.get('remboursement_id')

        if not remboursement_id:
            return JsonResponse({"status":"error",'message':"Informations manquantes"})
        
        refund = Rembourssements.objects.get(id = remboursement_id)

        paiements = Paiements.objects.filter(prospect_id = refund.client.id).values('id','num','montant_paye','date_paiement','mode_paiement','paiement_label','is_refund')

        paiements_liste = Paiements.objects.filter(prospect_id = refund.client.id)
        data = []
        for i in paiements_liste:
            data.append({
                'id' : i.id,
                'num' : i.num,
                'montant_paye' : i.montant_paye,
                'date_paiement' : i.date_paiement,
                'mode_paiement' : i.mode_paiement,
                'mode_paiement_label' : i.get_mode_paiement_display(),
                'paiement_label' : i.paiement_label,
                'is_refund' : i.is_refund,
            })

        return JsonResponse(data, safe=False)
        

    else:
        return JsonResponse({"status":"error"})