from django.shortcuts import render
from django.http import JsonResponse
from ..models import *
from django.db import transaction
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from itertools import chain
from datetime import datetime
from django.db.models import F, Value,CharField, Q
from django.db.models.functions import Coalesce
from itertools import chain
from django.db.models.functions import Concat
from django.contrib.humanize.templatetags.humanize import intcomma


@login_required(login_url="institut_app:login")
def PageBrouillardCaisse(request):
    return render(request, 'tenant_folder/comptabilite/caisse/brouillad_caisse.html')

@login_required(login_url="institut_app:login")
def PageBrouillardBanque(request):
    return render(request,'tenant_folder/comptabilite/caisse/brouillard_banque.html')

@login_required(login_url="institut_app:login")
def brouillard_caisse_json(request):

    # ---- 1. Paiements (Entrées en espèce) ----
    paiements = Paiements.objects.filter(mode_paiement='esp',).values(
        nom=F('paiement_label'),
        date=F('date_paiement'),
        montant=F('montant_paye'),
        type=Value('entree', output_field=models.CharField()),
        descri=Coalesce('paiement_label', Value('')),
        ref=F('num'),
        order_to = Concat(
                F('prospect__nom'), Value(' '), F('prospect__prenom'),
                output_field=CharField()
            ),
        entite = F('due_paiements__ref_echeancier__entite__designation')
    )

    # ---- 2. Dépenses (Sorties en espèce) ----
    depenses = Depenses.objects.filter(mode_paiement='esp').values(
        nom =F('label'),
        date=F('date_paiement'),
        montant=F('montant_ttc'),
        type=Value('sortie', output_field=models.CharField()),
        descr=F('description'),
        ref=F('piece'),
        order_to = F('fournisseur__designation'),
        entite = Value('ets', output_field=models.CharField())
    )

    # ---- 3. Fusion et tri chronologique ----
    mouvements = sorted(
        chain(paiements, depenses),
        key=lambda x: x['date'] or datetime.min
    )

    # ---- 4. Calcul du solde cumulatif ----
    solde = 0
    results = []

    for mv in mouvements:
        montant = float(mv['montant']) if mv['montant'] else 0

        if mv['type'] == 'entree':
            solde += montant
        else:
            solde -= montant

        results.append({
            "date": mv['date'],
            "type": mv['type'],
            "nom" : mv['nom'],
            #"description": mv['descr'],
            "montant": montant,
            #"reference": mv['reference'],
            "solde": solde,
            "order_to" : mv['order_to']
        })

       

    # ---- 5. Retour JSON propre ----
    return JsonResponse({
        "status": "success",
        "solde_final": solde,
        "mouvements": results
    }, safe=False)


@login_required(login_url="institut_app:login")
def brouillard_banque(request):
    pass

@login_required(login_url="institut_app:login")
def ImputationBancaire(request):
    return render(request,'tenant_folder/comptabilite/caisse/imputation_bancaire.html')


@login_required(login_url="institut_app:login")
def ApiReturnUndonePaiament(request):
    if request.method == "GET":

        paiements = OperationsBancaire.objects.filter(operation_type = "entree")
        depenses = OperationsBancaire.objects.filter(operation_type = "sortie")

        liste_paiements = []
        liste_depenses  = []

        for i in paiements:
            liste_paiements.append({
                'id' : i.id,
                'type' : i.get_operation_type_display(),
                'mode_paiement' : i.paiement.mode_paiement,
                'label_mode_paiement' : i.paiement.get_mode_paiement_display(),
                'paiement_id' : i.paiement.id,
                'paiement_ref' : i.paiement.reference_paiement,
                'client' : i.paiement.prospect.nom+' '+i.paiement.prospect.prenom,
                'client_id' : i.paiement.prospect.id,
                'entite' : i.paiement.due_paiements.ref_echeancier.entite.designation,
                'montant' : i.montant,
                'date_operation' : i.date_operation,
                'is_approche' : i.is_rapproche,
                'compte' : i.compte_bancaire.bank_name if i.compte_bancaire else None,
                
            })

        data = {
            'paiements' : liste_paiements,
            'depenses'  : liste_depenses,
        }

    
        return JsonResponse(data, safe=False)

    else:
        return JsonResponse({"status" : "error"})
    

@login_required(login_url="institut_app:login")
def ApiLoadEntrepises(request):
    if request.method == "GET":
        entreprises = Entreprise.objects.all().values('id','designation')

        return JsonResponse(list(entreprises), safe=False)
    else:
        return JsonResponse({"status" : "error"})

def PaiementsData(request):
    paiements = Paiements.objects.filter(mode_paiement = 'esp')
    pass


@login_required(login_url="institut_app:login")
def ClientDetails(request, pk):
    return render(request,"tenant_folder/comptabilite/clients/details_clients.html")

from institut_app.decorators import *

@login_required(login_url="institut_app:login")
@ajax_required
def ApiDetailsPaiement(request):
    if request.method == "GET":
        id = request.GET.get('id')
        
        obj=OperationsBancaire.objects.get(id = id)
        data = {
            'id' : obj.id,
            'operation_type' : obj.get_operation_type_display(),
            'paiement' : obj.paiement.id if obj.paiement.id else None,
            'montant' : obj.montant if obj.montant else None,
            'date_operation' : obj.date_operation if obj.date_operation else None,
            'reference_bancaire' : obj.reference_bancaire if obj.reference_bancaire else None,
            'justification' : obj.justification if obj.justification else None,
            'is_rapproche' : obj.is_rapproche if obj.is_rapproche else None,
            'is_paid' : obj.is_paid if obj.is_paid else None,
            'date_paiement' : obj.date_paiement if obj.date_paiement else None,

        }
        return JsonResponse(data, safe=False)

    else:
        return JsonResponse({"status" : "error"})


@login_required(login_url="institut_app:login")
@ajax_required
def ApiListBankAccount(request):
    if request.method == "GET":
        liste = BankAccount.objects.all().values('id','entreprise__designation','bank_name','bank_code')

        return JsonResponse(list(liste),safe=False)

    else:
        return JsonResponse({"status" : "error"})
