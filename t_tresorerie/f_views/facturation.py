from institut_app.decorators import module_permission_required
from django.shortcuts import render, redirect
from django.http import JsonResponse
from ..models import *
from t_conseil.models import Facture, ConseilConfiguration, TvaConseil, LignesFacture
from django.contrib import messages
from django.db import transaction
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
import json
from t_crm.models import RemiseAppliquer, Prospets, FicheDeVoeux, Promos
from django.db.models import Q, Sum, F, Case, When, Value, CharField, Count


@login_required(login_url="institut_app:login")
@module_permission_required('tre', 'view')
def PageFacturation(request):
    if request.method == "GET":
        promos = Promos.objects.filter(etat="active").order_by('-created_at')
        return render(request, "tenant_folder/comptabilite/facturation/liste_des_factures.html", {"filter_type": "all", "promos": promos})

@login_required(login_url="institut_app:login")
@module_permission_required('tre', 'view')
def PageFacturesAvoir(request):
    if request.method == "GET":
        promos = Promos.objects.filter(etat="active").order_by('-created_at')
        return render(request, "tenant_folder/comptabilite/facturation/liste_des_factures.html", {"filter_type": "avoir", "promos": promos})


@login_required(login_url="institut_app:login")
@module_permission_required('tre', 'view')
def ApiListeDesFactures(request):
    if request.method == "GET":
        try:
            factures = Facture.objects.filter(module_source='tresorerie').order_by('-created_at')
            
            all_enterprises = Entreprise.objects.all()
            enterprises = [{'id': ent.id, 'name': ent.designation} for ent in all_enterprises]
            
            avoir_invoices = Facture.objects.filter(type_facture='avoir', module_source='tresorerie')
            avoir_dict = {a.facture_source_id: a.num_facture for a in avoir_invoices if a.facture_source_id}
            
            data = []
            for f in factures:
                ent_id = f.entreprise.id if f.entreprise else None
                ent_name = f.entreprise.designation if f.entreprise else "Sans Entité"
                
                data.append({
                    'id': f.id,
                    'numero': f.num_facture,
                    'client': str(f.client) if f.client else "Client Inconnu",
                    'client_override': f.client_nom_override,
                    'client_prenom_override': f.client_prenom_override,
                    'date': f.date_emission.strftime("%Y-%m-%d") if f.date_emission else "",
                    'echeance': f.date_echeance.strftime("%Y-%m-%d") if f.date_echeance else "",
                    'montant': -float(f.total_ttc()) if f.type_facture == 'avoir' and hasattr(f, 'total_ttc') else (float(f.total_ttc()) if hasattr(f, 'total_ttc') else 0.0),
                    'timbre': float(f.get_timbre()),
                    'etat': f.etat,
                    'mode_paiement': f.mode_paiement,
                    'created_at': f.created_at.strftime("%Y-%m-%d") if hasattr(f, 'created_at') else "",
                    'entreprise_id': ent_id,
                    'entreprise_name': ent_name,
                    'has_refund': f.remboursements.exists(),
                    'type_facture': f.type_facture,
                    'is_avoir': f.type_facture == 'avoir',
                    'has_avoir_generated': f.id in avoir_dict,
                    'avoir_ref': avoir_dict.get(f.id, None),
                })
            
            return JsonResponse({'status': 'success', 'data': data, 'enterprises': enterprises})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

@login_required(login_url="institut_app:login")
@module_permission_required('tre', 'view')
def TresorerieViewFacture(request, pk):
    try:
        facture = Facture.objects.get(num_facture=pk, module_source='tresorerie')
    except Facture.DoesNotExist:
        messages.error(request, "Facture introuvable.")
        return redirect('t_tresorerie:PageFacturation')
        
    lignes_facture = facture.lignes_facture.all()
    
    config = None
    if facture.entreprise:
        config = ConseilConfiguration.objects.filter(entreprise=facture.entreprise).first()
    
    if not config:
        config, _ = ConseilConfiguration.objects.get_or_create(entreprise=None)
        
    tvas = TvaConseil.objects.all().order_by('valeur')
    
    # Calculate totals and breakdown
    total_ht = 0
    tva_breakdown = {}
    
    for ligne in lignes_facture:
        total_ht += ligne.montant_ht
        if facture.show_tva:
            rate = float(ligne.tva_percent)
            amount = float(ligne.montant_ht) * (rate / 100)
            if rate > 0:
                tva_breakdown[rate] = tva_breakdown.get(rate, 0) + amount
            
    total_tva = sum(tva_breakdown.values())
    timbre = facture.get_timbre()
    total_ttc = facture.total_ttc()
    
    if facture.type_facture == 'avoir':
        total_ht = -total_ht
        total_tva = -total_tva
        timbre = -timbre
        total_ttc = -total_ttc
        for k in tva_breakdown:
            tva_breakdown[k] = -tva_breakdown[k]
            
    sorted_tva = sorted([{'rate': r, 'amount': a} for r, a in tva_breakdown.items()], key=lambda x: x['rate'], reverse=True)
    from t_tresorerie.models import OperationsBancaire
    paiements_qs = facture.tresorerie_paiements.all().order_by('-date_paiement')
    paiements_lies = []
    for p in paiements_qs:
        p.is_cashed = True
        if p.mode_paiement in ['che', 'vir']:
            op = OperationsBancaire.objects.filter(paiement=p, operation_type='entree').first()
            if op and not op.is_paid:
                p.is_cashed = False
        paiements_lies.append(p)
    
    facture_avoir = Facture.objects.filter(facture_source=facture, type_facture='avoir').first()

    context = {
        "tenant": request.tenant,
        "facture": facture,
        "lignes_facture": lignes_facture,
        "config": config,
        "tvas": tvas,
        "total_ht": total_ht,
        "total_tva": total_tva,
        "timbre": timbre,
        "total_ttc": total_ttc,
        "tva_breakdown": sorted_tva,
        "paiements_lies": paiements_lies,
        "facture_avoir": facture_avoir
    }
    return render(request, 'tenant_folder/comptabilite/facturation/details_facture.html', context)


@login_required(login_url="institut_app:login")
@module_permission_required('tre', 'view')
def ApiGetProspectPaymentsByNin(request):
    if request.method == "GET":
        try:
            prospect_id = request.GET.get('prospect_id')
            if not prospect_id:
                return JsonResponse({'status': 'error', 'message': 'ID prospect manquant'})
                
            try:
                prospect = Prospets.objects.get(id=prospect_id)
            except Prospets.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Prospect introuvable'})
                
            if prospect.nin:
                prospects = Prospets.objects.filter(nin=prospect.nin)
            else:
                prospects = Prospets.objects.filter(id=prospect.id)
                
            payments = Paiements.objects.filter(prospect__in=prospects).select_related('prospect', 'promo', 'facture', 'entite').order_by('-date_paiement')
            
            total_paid = payments.aggregate(total=Sum('montant_paye'))['total'] or Decimal('0.00')
            
            tvas = [{'id': t.id, 'valeur': float(t.valeur)} for t in TvaConseil.objects.all().order_by('valeur')]
            
            payments_list = []
            for p in payments:
                payments_list.append({
                    'id': p.id,
                    'num': p.num or f"PAI-{p.id}",
                    'date': p.date_paiement.strftime("%Y-%m-%d") if p.date_paiement else "-",
                    'montant': float(p.montant_paye) if p.montant_paye else 0.0,
                    'mode': p.get_mode_paiement_display() if p.mode_paiement else "Autre",
                    'mode_raw': p.mode_paiement,
                    'promo_label': p.promo.label if p.promo else (p.prospect.specialite_obtenu or "Inconnue"),
                    'label': p.paiement_label or p.observation or "Règlement",
                    'has_invoice': p.facture is not None,
                    'num_facture': p.facture.num_facture if p.facture else None,
                    'entite_name': p.entite.designation if p.entite else "Sans Entité",
                    'entite_id': p.entite.id if p.entite else None,
                })
                
            return JsonResponse({
                'status': 'success',
                'prospect_info': {
                    'id': prospect.id,
                    'nom': prospect.nom,
                    'prenom': prospect.prenom or '',
                    'nin': prospect.nin or 'Non renseigné',
                    'telephone': prospect.telephone or 'Non renseigné',
                    'email': prospect.email or 'Non renseigné',
                },
                'total_paid': float(total_paid),
                'payments': payments_list,
                'tvas': tvas
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})


@login_required(login_url="institut_app:login")
@require_http_methods(["POST"])
@module_permission_required('tre', 'delete')
def ApiDeleteFacture(request):
    try:
        facture_id = request.POST.get('facture_id')
        if not facture_id:
            return JsonResponse({'status': 'error', 'message': 'ID de facture manquant.'})
            
        try:
            facture = Facture.objects.get(id=facture_id, module_source='tresorerie')
        except Facture.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Facture introuvable.'})
            
        if facture.etat != 'brouillon':
            return JsonResponse({'status': 'error', 'message': 'Une facture validée ne peut pas être supprimée.'})
            
        with transaction.atomic():
            facture.tresorerie_paiements.update(facture=None)
            facture.delete()
            
        return JsonResponse({
            'status': 'success', 
            'message': 'La facture a été supprimée avec succès et les règlements associés ont été libérés.'
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


@login_required(login_url="institut_app:login")
@require_http_methods(["POST"])
@module_permission_required('tre', 'approuv')
def ApiValidateFacture(request):
    try:
        facture_id = request.POST.get('facture_id')
        if not facture_id:
            return JsonResponse({'status': 'error', 'message': 'ID de facture manquant.'})
            
        try:
            facture = Facture.objects.get(id=facture_id, module_source='tresorerie')
        except Facture.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Facture introuvable.'})
            
        if facture.etat != 'brouillon':
            return JsonResponse({'status': 'error', 'message': f'La facture est déjà validée ou dans un autre état (Statut: {facture.get_etat_display()}).'})
            
        with transaction.atomic():
            facture.etat = 'paye'
            facture.save()
            
        return JsonResponse({
            'status': 'success', 
            'message': 'La facture a été validée avec succès.'
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


@login_required(login_url="institut_app:login")
@module_permission_required('tre', 'view')
def ApiGetDraftInvoiceDetails(request):
    if request.method == "GET":
        try:
            facture_id = request.GET.get('facture_id')
            if not facture_id:
                return JsonResponse({'status': 'error', 'message': 'ID de facture manquant'})
                
            try:
                facture = Facture.objects.get(id=facture_id, module_source='tresorerie')
            except Facture.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Facture introuvable'})
                
            if facture.etat != 'brouillon':
                return JsonResponse({'status': 'error', 'message': 'La facture n\'est pas en brouillon.'})
                
            prospect = facture.client
            if not prospect:
                return JsonResponse({'status': 'error', 'message': 'Client introuvable lié à cette facture.'})
                
            # Fetch all payments for this student's NIN (similar to ApiGetProspectPaymentsByNin)
            if prospect.nin:
                prospects = Prospets.objects.filter(nin=prospect.nin)
            else:
                prospects = Prospets.objects.filter(id=prospect.id)
                
            payments = Paiements.objects.filter(prospect__in=prospects).select_related('prospect', 'promo', 'facture', 'entite').order_by('-date_paiement')
            
            # Determine skip_timbre based on whether montant_timbre is 0
            skip_timbre = (facture.montant_timbre == 0)
            
            # Determine consolidation mode
            # If there's 1 line in lignes_facture but >1 associated payments, it is single_line.
            # Otherwise it's multi_line
            assoc_count = facture.tresorerie_paiements.count()
            lines_count = facture.lignes_facture.count()
            consolidation_mode = 'single_line' if (lines_count == 1 and assoc_count > 1) else 'multi_line'
            
            tvas = [{'id': t.id, 'valeur': float(t.valeur)} for t in TvaConseil.objects.all().order_by('valeur')]
            
            payments_list = []
            for p in payments:
                payments_list.append({
                    'id': p.id,
                    'num': p.num or f"PAI-{p.id}",
                    'date': p.date_paiement.strftime("%Y-%m-%d") if p.date_paiement else "-",
                    'montant': float(p.montant_paye) if p.montant_paye else 0.0,
                    'mode': p.get_mode_paiement_display() if p.mode_paiement else "Autre",
                    'mode_raw': p.mode_paiement,
                    'promo_label': p.promo.label if p.promo else (p.prospect.specialite_obtenu or "Inconnue"),
                    'label': p.paiement_label or p.observation or "Règlement",
                    'has_invoice': p.facture is not None,
                    'num_facture': p.facture.num_facture if p.facture else None,
                    'facture_id': p.facture.id if p.facture else None,
                    'entite_name': p.entite.designation if p.entite else "Sans Entité",
                    'entite_id': p.entite.id if p.entite else None,
                })
                
            return JsonResponse({
                'status': 'success',
                'invoice': {
                    'id': facture.id,
                    'numero': facture.num_facture,
                    'tva_percent': float(facture.tva),
                    'show_tva': facture.show_tva,
                    'skip_timbre': skip_timbre,
                    'consolidation_mode': consolidation_mode
                },
                'prospect_info': {
                    'id': prospect.id,
                    'nom': prospect.nom,
                    'prenom': prospect.prenom or '',
                    'nin': prospect.nin or 'Non renseigné',
                    'telephone': prospect.telephone or 'Non renseigné',
                    'email': prospect.email or 'Non renseigné',
                },
                'payments': payments_list,
                'tvas': tvas
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})


@login_required(login_url="institut_app:login")
@require_http_methods(["POST"])
@module_permission_required('tre', 'view')
def ApiDemanderRemboursement(request):
    try:
        facture_id = request.POST.get('facture_id')
        montant = request.POST.get('montant')
        motif = request.POST.get('motif')
        mode_paiement = request.POST.get('mode_paiement')

        if not all([facture_id, montant, motif, mode_paiement]):
            return JsonResponse({'status': 'error', 'message': 'Informations manquantes'})

        facture = Facture.objects.get(id=facture_id)
        
        if not facture.client:
            return JsonResponse({'status': 'error', 'message': 'Cette facture n\'est pas associée à un client (prospect).'})

        existing_request = Rembourssements.objects.filter(facture=facture, is_done=False).exists()
        if existing_request:
            return JsonResponse({'status': 'error', 'message': 'Une demande de remboursement est déjà en cours pour cette facture.'})

        Rembourssements.objects.create(
            client=facture.client,
            facture=facture,
            motif_rembourssement=motif,
            allowed_amount=Decimal(montant),
            mode_rembourssement=mode_paiement,
            entite=facture.entreprise,
            etat='enc',
            is_done=False,
            is_appliced=False
        )

        return JsonResponse({'status': 'success', 'message': 'Demande de remboursement initiée avec succès.'})
    except Facture.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Facture introuvable'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

@login_required(login_url="institut_app:login")
@module_permission_required('tre', 'view')
def PageModifierFacture(request, pk):
    try:
        facture = Facture.objects.get(id=pk, module_source='tresorerie')
    except Facture.DoesNotExist:
        messages.error(request, "Facture introuvable.")
        return redirect('t_tresorerie:PageFacturation')
        
    if facture.etat != 'brouillon':
        messages.warning(request, "Attention : Cette facture est déjà validée ou payée. Toute modification de ses lignes peut impacter la cohérence de la comptabilité.")
        
    lignes_facture = facture.lignes_facture.all().order_by('id')
    prospect = facture.client
    
    # Get all payments for this prospect
    payments = []
    if prospect:
        if prospect.nin:
            prospects = Prospets.objects.filter(nin=prospect.nin)
        else:
            prospects = Prospets.objects.filter(id=prospect.id)
        payments = Paiements.objects.filter(prospect__in=prospects).select_related('prospect', 'promo', 'facture', 'entite').order_by('-date_paiement')
    
    tvas = TvaConseil.objects.all().order_by('valeur')
    
    assoc_count = facture.tresorerie_paiements.count()
    lines_count = lignes_facture.count()
    consolidation_mode = 'single_line' if (lines_count == 1 and assoc_count > 1) else 'multi_line'
    
    # Calculate totals and breakdown for Synthèse Financière
    total_ht = 0
    tva_breakdown = {}
    
    for ligne in lignes_facture:
        total_ht += ligne.montant_ht
        if facture.show_tva:
            rate = float(ligne.tva_percent)
            amount = float(ligne.montant_ht) * (rate / 100)
            if rate > 0:
                tva_breakdown[rate] = tva_breakdown.get(rate, 0) + amount
            
    total_tva = sum(tva_breakdown.values())
    timbre = facture.get_timbre()
    total_ttc = facture.total_ttc()
    
    sorted_tva = sorted([{'rate': r, 'amount': a} for r, a in tva_breakdown.items()], key=lambda x: x['rate'], reverse=True)

    context = {
        "tenant": request.tenant,
        "facture": facture,
        "lignes_facture": lignes_facture,
        "prospect": prospect,
        "payments": payments,
        "tvas": tvas,
        "consolidation_mode": consolidation_mode,
        "total_ht": total_ht,
        "total_tva": total_tva,
        "timbre": timbre,
        "total_ttc": total_ttc,
        "tva_breakdown": sorted_tva,
    }
    return render(request, 'tenant_folder/comptabilite/facturation/modifier_facture.html', context)

@login_required(login_url="institut_app:login")
@require_http_methods(["POST"])
@module_permission_required('tre', 'change')
def ApiUpdateFactureClientOverride(request):
    try:
        data = json.loads(request.body)
        facture_id = data.get('facture_id')
        client_nom_override = data.get('client_nom_override', '')
        client_prenom_override = data.get('client_prenom_override', '')
        client_nin_override = data.get('client_nin_override', '')
        
        if not facture_id:
            return JsonResponse({'status': 'error', 'message': 'ID de facture manquant.'})
            
        facture = Facture.objects.get(id=facture_id, module_source='tresorerie')
        
        with transaction.atomic():
            facture.client_nom_override = client_nom_override if client_nom_override else None
            facture.client_prenom_override = client_prenom_override if client_prenom_override else None
            facture.client_nin_override = client_nin_override if client_nin_override else None
            facture.save()
            
        return JsonResponse({'status': 'success', 'message': 'Informations du client mises à jour avec succès.'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

@login_required(login_url="institut_app:login")
@require_http_methods(["POST"])
@module_permission_required('tre', 'view')
def ApiUpdateFactureLignes(request):
    try:
        data = json.loads(request.body)
        facture_id = data.get('facture_id')
        lignes = data.get('lignes', [])
        client_nom_override = data.get('client_nom_override', '')
        client_prenom_override = data.get('client_prenom_override', '')
        client_nin_override = data.get('client_nin_override', '')
        
        if not facture_id:
            return JsonResponse({'status': 'error', 'message': 'ID de facture manquant.'})
            
        facture = Facture.objects.get(id=facture_id, module_source='tresorerie')
        
        # if facture.etat != 'brouillon':
        #     return JsonResponse({'status': 'error', 'message': 'Seules les factures en brouillon peuvent être modifiées.'})
            
        with transaction.atomic():
            facture.client_nom_override = client_nom_override if client_nom_override else None
            facture.client_prenom_override = client_prenom_override if client_prenom_override else None
            facture.client_nin_override = client_nin_override if client_nin_override else None
            facture.save()

            for ligne_data in lignes:
                ligne_id = ligne_data.get('id')
                description = ligne_data.get('description')
                long_description = ligne_data.get('long_description')
                if ligne_id and description is not None:
                    LignesFacture.objects.filter(id=ligne_id, facture=facture).update(
                        description=description,
                        long_description=long_description
                    )
            
        return JsonResponse({'status': 'success', 'message': 'Lignes de facture mises à jour avec succès.'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

@login_required(login_url="institut_app:login")
@module_permission_required('tre', 'view')
def PrintFactureTresorerie(request, pk):
    from pdf_editor.models import DocumentTemplate, DocumentGeneration
    from pdf_editor.utils import render_template_with_context
    from django.utils import timezone

    try:
        facture = Facture.objects.get(num_facture=pk, module_source='tresorerie')
    except Facture.DoesNotExist:
        messages.error(request, 'Facture introuvable.')
        return redirect('t_tresorerie:PageFacturation')

    if facture.etat == 'brouillon':
        messages.warning(request, "La facture doit être validée avant de pouvoir être imprimée.")
        return redirect('t_tresorerie:TresorerieViewFacture', pk=facture.num_facture)

    try:
        template_obj = DocumentTemplate.objects.get(slug='dolibare_facture', is_active=True)
    except DocumentTemplate.DoesNotExist:
        messages.error(request, "Template 'dolibare_facture' introuvable dans l'éditeur de documents.")
        return redirect('t_tresorerie:TresorerieViewFacture', pk=pk)

    lignes_facture = facture.lignes_facture.all()
    
    total_ht = 0
    total_tva = 0
    tva_breakdown = {}
    
    for ligne in lignes_facture:
        total_ht += float(ligne.montant_ht)
        if facture.show_tva:
            rate = float(getattr(ligne, 'tva_percent', 0))
            amount = float(ligne.montant_ht) * (rate / 100)
            if rate > 0:
                tva_breakdown[rate] = tva_breakdown.get(rate, 0) + amount

    total_tva = sum(tva_breakdown.values())
    timbre = float(facture.get_timbre()) if hasattr(facture, 'get_timbre') else 0
    total_ttc = total_ht + total_tva + timbre
    total_remise = getattr(facture, 'montant_remise_globale', 0)

    emetteur = getattr(facture, 'entreprise', None)


    
    from t_conseil.models import ConseilConfiguration
    config_fin = ConseilConfiguration.objects.filter(entreprise=emetteur).first() if emetteur else ConseilConfiguration.objects.filter(entreprise=None).first()
    
    banque_nom = ''
    banque_iban = ''
    if config_fin and config_fin.compte_bancaire_defaut:
        banque_nom = config_fin.compte_bancaire_defaut.bank_name
        banque_iban = config_fin.compte_bancaire_defaut.bank_iban

    if facture.client_nom_override:
        client_nom = f"{facture.client_nom_override} {facture.client_prenom_override or ''}".strip()
        client_nin = facture.client_nin_override or getattr(facture.client, 'nin', '')
        client_nif = getattr(facture.client, 'nif', '')
        client_initial = f"{getattr(facture.client, 'nom', '')} {getattr(facture.client, 'prenom', '')}".strip()
    else:
        client_nom = str(facture.client.entreprise) if getattr(facture.client, 'entreprise', None) else f"{getattr(facture.client, 'nom', '')} {getattr(facture.client, 'prenom', '')}"
        client_nin = getattr(facture.client, 'nin', '')
        client_nif = getattr(facture.client, 'nif', '')
        client_initial = ""

    context_data = {
        'entreprise_nom': emetteur.designation if emetteur else 'SALDAE',
        'entreprise_adresse': getattr(emetteur, 'adresse', ''),
        'entreprise_telephone': getattr(emetteur, 'telephone', ''),
        'entreprise_email': getattr(emetteur, 'email', ''),
        'entreprise_rc': getattr(emetteur, 'rc', ''),
        'entreprise_nif': getattr(emetteur, 'nif', ''),
        'entreprise_nis': getattr(emetteur, 'nis', ''),
        'entreprise_art_imp': getattr(emetteur, 'art', ''),
        'entreprise_logo': request.build_absolute_uri(emetteur.logo.url) if emetteur and hasattr(emetteur, 'logo') and emetteur.logo else '',
        
        'banque_nom': banque_nom,
        'banque_iban': banque_iban,
        
        'facture_numero': facture.num_facture,
        'date_emission': facture.date_facturation.strftime("%d/%m/%Y") if hasattr(facture, 'date_facturation') and facture.date_facturation else "",
        'date_echeance': facture.date_echeance.strftime("%d/%m/%Y") if facture.date_echeance else "",
        'conditions_commerciales': getattr(facture, 'conditions_commerciales', ''),
        'mode_paiement': facture.get_mode_paiement_display() if hasattr(facture, 'get_mode_paiement_display') else getattr(facture, 'mode_paiement', ''),
        
        'client_nom': client_nom,
        'client_initial': client_initial,
        'client_adresse': getattr(facture.client, 'adresse', ''),
        'client_telephone': getattr(facture.client, 'telephone', ''),
        'client_email': getattr(facture.client, 'email', ''),
        'client_rc': getattr(facture.client, 'rc', ''),
        'client_nif': client_nif,
        'client_nin': client_nin,
        'client_nis': getattr(facture.client, 'nis', ''),
        'client_art_imp': getattr(facture.client, 'art_imp', ''),
        'client_logo': request.build_absolute_uri(facture.client.logo_entreprise.url) if hasattr(facture.client, 'logo_entreprise') and getattr(facture.client, 'logo_entreprise') else '',
        
        'lignes': [
            {
                'designation': getattr(ligne.thematique, 'label', '') if hasattr(ligne, 'thematique') and ligne.thematique else getattr(ligne, 'description', ''),
                'description': (getattr(ligne, 'long_description') if getattr(ligne, 'long_description', None) else (getattr(ligne, 'description', '') if hasattr(ligne, 'thematique') and ligne.thematique else '')).strip() + (f"\n(Au profit de : {client_initial})" if client_initial else ""),
                'quantite': float(ligne.quantite),
                'prix_unitaire': float(ligne.prix_unitaire_ht) if hasattr(ligne, 'prix_unitaire_ht') else float(getattr(ligne, 'prix_unitaire', 0)),
                'tva_percent': float(getattr(ligne, 'tva_percent', 0)) if facture.show_tva else 0,
                'remise_percent': float(getattr(ligne, 'remise_percent', 0)) if getattr(facture, 'show_remise', False) else 0,
                'montant': float(ligne.montant_ht) if hasattr(ligne, 'montant_ht') else float(getattr(ligne, 'montant', 0))
            } for ligne in lignes_facture
        ],
        'total_ht': round(total_ht, 2),
        'total_tva': round(total_tva, 2),
        'total_ttc': round(total_ttc, 2),
        'total_remise': round(total_remise, 2),
        'timbre': round(timbre, 2),
        'show_tva': facture.show_tva,
        'show_remise': getattr(facture, 'show_remise', False),
    }

    try:
        rendered_content, error = render_template_with_context(template_obj.content, context_data)
        if error:
            messages.error(request, f"Erreur de génération : {error}")
            return redirect('t_tresorerie:TresorerieViewFacture', pk=pk)

        doc_gen = DocumentGeneration.objects.create(
            template=template_obj,
            context_data=context_data,
            rendered_content=rendered_content,
            generated_by=request.user
        )

        return redirect('pdf_editor:document-export', pk=doc_gen.pk)
    except Exception as e:
        messages.error(request, f"Erreur lors de la génération PDF : {str(e)}")
        return redirect('t_tresorerie:TresorerieViewFacture', pk=pk)
