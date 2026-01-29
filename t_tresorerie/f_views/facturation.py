from django.shortcuts import render, redirect
from django.http import JsonResponse
from ..models import *
from t_conseil.models import Facture, ConseilConfiguration, TvaConseil
from django.contrib import messages
from django.db import transaction
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
import json
from t_crm.models import RemiseAppliquer, Prospets,FicheDeVoeux
from django.db.models import Q, Sum, F, Case, When, Value, CharField, Count


@login_required(login_url="institut_app:login")
def PageFacturation(request):
    return render(request, "tenant_folder/comptabilite/facturation/liste_des_factures.html")


@login_required(login_url="institut_app:login")
def ApiListeDesFactures(request):
    if request.method == "GET":
        try:
            factures = Facture.objects.filter(module_source='tresorerie').order_by('-created_at')
            
            all_enterprises = Entreprise.objects.all()
            enterprises = [{'id': ent.id, 'name': ent.designation} for ent in all_enterprises]
            
            data = []
            for f in factures:
                ent_id = f.entreprise.id if f.entreprise else None
                ent_name = f.entreprise.designation if f.entreprise else "Sans Entité"
                
                data.append({
                    'id': f.id,
                    'numero': f.num_facture,
                    'client': str(f.client) if f.client else "Client Inconnu",
                    'date': f.date_emission.strftime("%Y-%m-%d") if f.date_emission else "",
                    'echeance': f.date_echeance.strftime("%Y-%m-%d") if f.date_echeance else "",
                    'montant': float(f.total_ttc()) if hasattr(f, 'total_ttc') else 0.0,
                    'etat': f.etat,
                    'created_at': f.created_at.strftime("%Y-%m-%d") if hasattr(f, 'created_at') else "",
                    'entreprise_id': ent_id,
                    'entreprise_name': ent_name
                })
            
            return JsonResponse({'status': 'success', 'data': data, 'enterprises': enterprises})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

@login_required(login_url="institut_app:login")
def DetailsFactureTresorerie(request, pk):
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
    total_ttc = float(total_ht) + total_tva
    sorted_tva = sorted([{'rate': r, 'amount': a} for r, a in tva_breakdown.items()], key=lambda x: x['rate'], reverse=True)

    context = {
        "tenant": request.tenant,
        "facture": facture,
        "lignes_facture": lignes_facture,
        "config": config,
        "tvas": tvas,
        "total_ht": total_ht,
        "total_tva": total_tva,
        "total_ttc": total_ttc,
        "tva_breakdown": sorted_tva
    }
    return render(request, 'tenant_folder/comptabilite/facturation/details_facture.html', context)