from institut_app.decorators import module_permission_required
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


@module_permission_required('tre', 'view')
def listeDesRembourssement(request):
    return render(request, "tenant_folder/comptabilite/tresorerie/liste-des-rembourssement.html")


@login_required
@require_http_methods(["GET"])
@module_permission_required('tre', 'view')
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

        paiements_base = Paiements.objects.filter(prospect=client.id, is_refund=False, context="frais_f")
        paiements = paiements_base.filter(Q(is_done=True) | Q(mode_paiement='esp')).aggregate(total=Sum('montant_paye'))['total'] or 0
        paiements_attente = paiements_base.filter(is_done=False).exclude(mode_paiement='esp').aggregate(total=Sum('montant_paye'))['total'] or 0
        
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
            "mode_rembourssement_key" : r.mode_rembourssement,
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
            'total_attente' : float(paiements_attente),
        })

    return JsonResponse(data, safe=False)


@login_required(login_url="institut_app:login")
@module_permission_required('tre', 'view')
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

    paiements_base = Paiements.objects.filter(prospect=obj.client, is_refund=False).exclude(Q(context='frais_i') | Q(is_frais_inscription=True))
    total_paye = paiements_base.filter(Q(is_done=True) | Q(mode_paiement='esp')).aggregate(total=Sum('montant_paye'))['total'] or 0
    total_attente = paiements_base.filter(is_done=False).exclude(mode_paiement='esp').aggregate(total=Sum('montant_paye'))['total'] or 0
    paiements = Paiements.objects.filter(prospect=obj.client).exclude(Q(context='frais_i') | Q(is_frais_inscription=True)).order_by('due_paiements__date_echeance', 'id')
    last_paiements = Paiements.objects.filter(prospect=obj.client, is_refund=False).exclude(Q(context='frais_i') | Q(is_frais_inscription=True)).last()

    groupe_line = GroupeLine.objects.filter(student=obj.client)
    has_factured_payments = paiements.filter(facture__isnull=False).exists()

    context = {
        'obj': obj,
        'voeux': voeux,
        'formation_label': formation_label,
        'specialite_label': specialite_label,
        'promotion_label': promotion_label,
        'total_paye' : total_paye,
        'total_attente' : total_attente,
        'paiements' : paiements,
        'entreprise' : entreprise,
        'last_payment' : last_paiements,
        'groupe' : groupe_line,
        'has_factured_payments': has_factured_payments,
    }
    return render(request, 'tenant_folder/comptabilite/rembourssement/details_rembourssement.html', context)

@login_required(login_url="institut_app:login")
@module_permission_required('tre', 'view')
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
                'is_factured' : bool(i.facture),
                'facture_num' : i.facture.num_facture if i.facture else None,
            })

        return JsonResponse(data, safe=False)
        

    else:
        return JsonResponse({"status":"error"})

@login_required(login_url="institut_app:login")
@module_permission_required('tre', 'view')
def ApiSearchProspectForRefund(request):
    if request.method == "GET":
        query = request.GET.get('q', '').strip()
        promo_id = request.GET.get('promo_id', '').strip()
        
        if not query and not promo_id:
            return JsonResponse({'prospects': []})
            
        excluded_prospect_ids = Rembourssements.objects.filter(
            etat__in=['enc', 'acp']
        ).values_list('client_id', flat=True)
        
        prospects = Prospets.objects.filter(statut__in=['instance', 'convertit']).exclude(id__in=excluded_prospect_ids)
        
        if query:
            prospects = prospects.filter(
                Q(nom__icontains=query) | 
                Q(prenom__icontains=query) | 
                Q(email__icontains=query)
            )
            
        if promo_id:
            p_ids1 = FicheDeVoeux.objects.filter(promo_id=promo_id).values_list('prospect_id', flat=True)
            p_ids2 = FicheVoeuxDouble.objects.filter(promo_id=promo_id).values_list('prospect_id', flat=True)
            prospect_ids = list(p_ids1) + list(p_ids2)
            prospects = prospects.filter(id__in=prospect_ids)
            
        prospects = prospects.distinct()[:20] # Limit to 20 results
        
        data = []
        for prospect in prospects:
            # Academics
            if prospect.is_double:
                voeux = FicheVoeuxDouble.objects.filter(prospect=prospect, is_confirmed=True).last()
                if not voeux:
                    voeux = FicheVoeuxDouble.objects.filter(prospect=prospect).last()
                formation_label = "Double Diplomation"
                specialite_label = f"{voeux.specialite.specialite1.label} / {voeux.specialite.specialite2.label}" if voeux and voeux.specialite else "Inconnue"
                promo_label = voeux.promo.code if voeux and voeux.promo else "Inconnue"
            else:
                voeux = FicheDeVoeux.objects.filter(prospect=prospect, is_confirmed=True).last()
                if not voeux:
                    voeux = FicheDeVoeux.objects.filter(prospect=prospect).last()
                formation_label = voeux.specialite.formation.nom if voeux and voeux.specialite and voeux.specialite.formation else "Inconnue"
                specialite_label = voeux.specialite.label if voeux and voeux.specialite else "Inconnue"
                promo_label = voeux.promo.code if voeux and voeux.promo else "Inconnue"

            # Groupe
            groupe_line = GroupeLine.objects.filter(student=prospect).last()
            groupe_label = groupe_line.groupe.nom if groupe_line and groupe_line.groupe else "Non assigné"

            # Financials
            due_paiements_qs = DuePaiements.objects.filter(client=prospect, is_annulated=False)
            total_due = due_paiements_qs.aggregate(total=Sum('montant_due'))['total'] or Decimal('0.0')
            
            paiements_qs_all = Paiements.objects.filter(prospect=prospect, is_refund=False).exclude(Q(context='frais_i') | Q(is_frais_inscription=True) | Q(paiement_label__icontains="inscription"))
            paiements_qs_encaisse = paiements_qs_all.filter(Q(is_done=True) | Q(mode_paiement='esp'))
            paiements_qs_attente = paiements_qs_all.filter(is_done=False).exclude(mode_paiement='esp')
            
            total_paye = paiements_qs_encaisse.aggregate(total=Sum('montant_paye'))['total'] or Decimal('0.0')
            total_attente = paiements_qs_attente.aggregate(total=Sum('montant_paye'))['total'] or Decimal('0.0')

            # Invoice
            has_invoice = paiements_qs_all.filter(facture__isnull=False).exists()
            invoice_status = "Facture générée" if has_invoice else "Non facturé"

            data.append({
                'id': prospect.id,
                'nom': prospect.nom,
                'prenom': prospect.prenom,
                'email': prospect.email,
                'telephone': prospect.telephone,
                'nin': prospect.nin,
                'formation': formation_label,
                'specialite': specialite_label,
                'promo': promo_label,
                'groupe': groupe_label,
                'total_due': float(total_due),
                'total_paye': float(total_paye),
                'total_attente': float(total_attente),
                'invoice_status': invoice_status,
                'has_invoice': has_invoice,
            })
            
        return JsonResponse({'prospects': data})
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@login_required(login_url="institut_app:login")
@require_http_methods(["POST"])
@module_permission_required('tre', 'delete')
def ApiCancelRefund(request, pk):
    try:
        obj = Rembourssements.objects.get(id=pk)
        if obj.is_appliced:
            return JsonResponse({'status': 'error', 'message': "Impossible d'annuler un remboursement déjà déclenché (dépense générée)."}, status=400)
        
        # Log action before deletion
        UserActionLog.objects.create(
            user=request.user,
            action_type='DELETE',
            target_model='Rembourssements',
            target_id=str(obj.id),
            details=f"Annulation/Suppression de la demande de remboursement de {obj.allowed_amount} DA pour {obj.client.nom} {obj.client.prenom}.",
            ip_address=request.META.get('REMOTE_ADDR')
        )
        
        obj.delete()
        return JsonResponse({'status': 'success', 'message': "La demande de remboursement a été annulée et réinitialisée."})
    except Rembourssements.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': "Demande de remboursement introuvable."}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
