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
    
    remboursements = Rembourssements.objects.select_related('client', 'facture').all()
    data = []

    for r in remboursements:
        if not r.client:
            continue
        client = r.client
        
        # 1. Fetch wish sheet (FicheDeVoeux or FicheVoeuxDouble) with a fallback if cancelled
        if client.is_double:
            voeux = FicheVoeuxDouble.objects.filter(prospect=client, is_confirmed=True).last()
            if not voeux:
                voeux = FicheVoeuxDouble.objects.filter(prospect=client).last()
                
            promo_code = voeux.promo.code if voeux and voeux.promo else None
            promo_label = voeux.promo.label if voeux and voeux.promo else None
            promo_session = voeux.promo.get_session_display() if voeux and voeux.promo else None
            promo_start = voeux.promo.begin_year if voeux and voeux.promo else None
            promo_end = voeux.promo.end_year if voeux and voeux.promo else None
            specialite = f"{voeux.specialite.specialite1.label} / {voeux.specialite.specialite2.label}" if voeux and voeux.specialite else None
            formation = "Double Diplomation"
        else:
            voeux = FicheDeVoeux.objects.filter(prospect=client, is_confirmed=True).last()
            if not voeux:
                voeux = FicheDeVoeux.objects.filter(prospect=client).last()
                
            promo_code = voeux.promo.code if voeux and voeux.promo else None
            promo_label = voeux.promo.label if voeux and voeux.promo else None
            promo_session = voeux.promo.get_session_display() if voeux and voeux.promo else None
            promo_start = voeux.promo.begin_year if voeux and voeux.promo else None
            promo_end = voeux.promo.end_year if voeux and voeux.promo else None
            specialite = voeux.specialite.label if voeux and voeux.specialite else None
            formation = voeux.specialite.formation.nom if voeux and voeux.specialite and voeux.specialite.formation else None

        paiements = Paiements.objects.filter(prospect=client.id, is_refund=False, context="frais_f").aggregate(total=Sum('montant_paye'))['total'] or 0
        
        data.append({
            "client_id": client.id,
            "nom": client.nom,
            "prenom": client.prenom,
            "telephone" : client.telephone,
            "email" : client.email,
            "remboursement_id": r.id,
            "allowed_amount": float(r.allowed_amount) if r.allowed_amount else 0,
            "updated_at": r.updated_at.strftime("%Y-%m-%d") if r.updated_at else None,
            "mode_rembourssement" : r.get_mode_rembourssement_display(),
            "motif_rembourssement" : r.motif_rembourssement,
            "observation" : r.observation,
            'promotion' : promo_code,
            'promotion_label' : promo_label,
            'promotion_session' : promo_session,
            'promotion_start' : promo_start,
            'promotion_end' : promo_end,
            'specialite' : specialite,
            'formation' : formation,
            'facture_num' : r.facture.num_facture if r.facture else None,
            'facture_id' : r.facture.id if r.facture else None,
            'etat' : r.get_etat_display(),
            'etat_key' : r.etat,
            'is_done' : r.is_done,
            'is_appliced' : r.is_appliced,
            'total_paye' : float(paiements) - float(r.allowed_amount if r.allowed_amount else 0),
        })

    return JsonResponse(data, safe=False)


@login_required(login_url="institut_app:login")
def DetailsRembourssement(request, pk):
    obj = Rembourssements.objects.get(id = pk)
    if obj.client.is_double:
        voeux = FicheVoeuxDouble.objects.filter(prospect=obj.client, is_confirmed=True).last()
        if not voeux:
            voeux = FicheVoeuxDouble.objects.filter(prospect=obj.client).last()
        if voeux:
            entreprise = Entreprise.objects.get(id=voeux.specialite.specialite1.formation.entite_legal.id)
            formation_label = "Double Diplomation"
            specialite_label = f"{voeux.specialite.specialite1.label} / {voeux.specialite.specialite2.label}"
            promotion_label = f"{voeux.promo.get_session_display()}-{voeux.promo.begin_year}" if voeux.promo else "-"
        else:
            entreprise = obj.entite
            formation_label = "Inconnue"
            specialite_label = "Inconnue"
            promotion_label = "-"
    else:
        voeux = FicheDeVoeux.objects.filter(prospect=obj.client, is_confirmed=True).last()
        if not voeux:
            voeux = FicheDeVoeux.objects.filter(prospect=obj.client).last()
        if voeux:
            entreprise = Entreprise.objects.get(id=voeux.specialite.formation.entite_legal.id)
            formation_label = voeux.specialite.formation.nom if voeux.specialite and voeux.specialite.formation else "-"
            specialite_label = voeux.specialite.label if voeux.specialite else "-"
            promotion_label = f"{voeux.promo.get_session_display()}-{voeux.promo.begin_year}" if voeux.promo else "-"
        else:
            entreprise = obj.entite
            formation_label = "Inconnue"
            specialite_label = "Inconnue"
            promotion_label = "-"

    total_paye = Paiements.objects.filter(prospect=obj.client, is_refund=False).aggregate(total=Sum('montant_paye'))['total'] or 0
    paiements = Paiements.objects.filter(prospect=obj.client).order_by('due_paiements__date_echeance', 'id')
    last_paiements = Paiements.objects.filter(prospect=obj.client, is_refund=False).last()

    groupe_line = GroupeLine.objects.filter(student=obj.client)

    context = {
        'obj': obj,
        'voeux': voeux,
        'formation_label': formation_label,
        'specialite_label': specialite_label,
        'promotion_label': promotion_label,
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

        paiements = Paiements.objects.filter(prospect_id = refund.client.id).order_by('due_paiements__date_echeance', 'id').values('id','num','montant_paye','date_paiement','mode_paiement','paiement_label','is_refund')

        paiements_liste = Paiements.objects.filter(prospect_id = refund.client.id).order_by('due_paiements__date_echeance', 'id')
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