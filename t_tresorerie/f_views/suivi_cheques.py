from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from institut_app.decorators import module_permission_required
from django.db.models import F, Case, When, Value, CharField
from django.db.models.functions import Concat
from t_tresorerie.models import OperationsBancaire, SuiviChequeSortant
from datetime import datetime
from django.utils import timezone
from django.db import transaction

@login_required(login_url="institut_app:login")
@module_permission_required('tre', 'view')
def PageSuiviChequesEmis(request):
    return render(request, "tenant_folder/comptabilite/caisse/suivi_cheques_emis.html")

@login_required(login_url="institut_app:login")
@module_permission_required('tre', 'view')
def ApiListChequesEmis(request):
    statut = request.GET.get('statut', 'tous')
    type_op = request.GET.get('type', 'cheque')
    
    # Base query for all sortie OperationsBancaire linked to a check
    # We rely on SuiviChequeSortant which is created automatically for check operations
    qs = SuiviChequeSortant.objects.select_related('depense', 'remboursement').all()
    
    if statut != 'tous':
        qs = qs.filter(statut=statut)
        
    data = []
    for sc in qs:
        montant = 0
        reference = ''
        beneficiaire = 'Inconnu'
        entite_name = ''
        mode = None
        
        if sc.depense:
            mode = sc.depense.mode_paiement
            montant = sc.depense.montant_ttc or sc.depense.montant_ht
            reference = sc.depense.reference
            if sc.depense.fournisseur:
                beneficiaire = sc.depense.fournisseur.designation
            elif sc.depense.client:
                beneficiaire = f"{sc.depense.client.nom} {sc.depense.client.prenom}"
                entite_name = sc.depense.entite.designation
                
        elif sc.remboursement:
            mode = sc.remboursement.mode_rembourssement
            montant = sc.remboursement.allowed_amount
            reference = ''
            if sc.remboursement.client:
                beneficiaire = f"{sc.remboursement.client.nom} {sc.remboursement.client.prenom}"
                entite_name = sc.remboursement.entite.designation
            
        if type_op == 'cheque' and mode != 'che':
            continue
        elif type_op == 'virement' and mode != 'vir':
            continue

        data.append({
            'id': sc.id,
            'statut': sc.statut,
            'statut_label': sc.get_statut_display(),
            'montant': montant,
            'reference': reference,
            'beneficiaire': beneficiaire,
            'date_emis': sc.date_emis.strftime('%Y-%m-%d') if sc.date_emis else None,
            'date_attente': sc.date_attente_signature.strftime('%Y-%m-%d') if sc.date_attente_signature else None,
            'date_remis': sc.date_remis.strftime('%Y-%m-%d') if sc.date_remis else None,
            'date_decaisse': sc.date_decaisse.strftime('%Y-%m-%d') if sc.date_decaisse else None,
            'entite': entite_name
        })
        
    return JsonResponse(data, safe=False)

@login_required(login_url="institut_app:login")
@module_permission_required('tre', 'change')
@transaction.atomic
def ApiUpdateChequeStatut(request):
    if request.method == "POST":
        suivi_id = request.POST.get('id')
        nouveau_statut = request.POST.get('statut')
        
        try:
            sc = SuiviChequeSortant.objects.get(id=suivi_id)
            sc.statut = nouveau_statut
            now = timezone.now()
            
            if nouveau_statut == 'attente_signature':
                sc.date_attente_signature = now
            elif nouveau_statut == 'remis':
                sc.date_remis = now
            elif nouveau_statut in ['decaisse', 'effectue']:
                sc.date_decaisse = now
                
            sc.save()
            return JsonResponse({"status": "success", "message": "Statut mis à jour avec succès"})
        except SuiviChequeSortant.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Chèque introuvable"})
    return JsonResponse({"status": "error", "message": "Méthode non autorisée"})
