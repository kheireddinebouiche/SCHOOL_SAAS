from django.shortcuts import render
from django.http import JsonResponse
from django.apps import apps
from ..models import *
from django.db import transaction
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from itertools import chain
from datetime import datetime
from django.db import models
from django.db.models import F, Value, CharField, Q
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
    # Load t_conseil Paiement model
    try:
        ConseilPaiement = apps.get_model('t_conseil', 'Paiement')
    except (LookupError, ImportError):
        ConseilPaiement = None

    # ---- 1. Paiements (Entrées en espèce) ----
    paiements = Paiements.objects.filter(mode_paiement='esp').values(
        nom=F('paiement_label'),
        date=F('date_paiement'),
        mouvement_montant=F('montant_paye'),
        type=Value('entree', output_field=CharField()),
        descri=Coalesce('paiement_label', Value('')),
        ref=F('num'),
        order_to=Concat(
            F('prospect__nom'), Value(' '), F('prospect__prenom'),
            output_field=CharField()
        ),
        entite_name=F('due_paiements__ref_echeancier__entite__designation')
    )

    # ---- 1b. AutreProduit (Entrées en espèce) ----
    autres_produits = AutreProduit.objects.filter(mode_paiement='cach').values(
        nom=F('label'),
        date=F('date_paiement'),
        mouvement_montant=F('montant_paiement'),
        type=Value('entree', output_field=CharField()),
        descri=F('label'),
        ref=F('num'),
        order_to=Concat(
            F('client__nom'), Value(' '), F('client__prenom'),
            output_field=CharField()
        ),
        entite_name=F('entite__designation')
    )

    # ---- 1c. Consulting Paiement (Entrées en espèce) ----
    consulting_paiements = []
    if ConseilPaiement:
        consulting_paiements = ConseilPaiement.objects.filter(mode_paiement='espece').values(
            nom=Value('Paiement Facture', output_field=CharField()),
            date=F('date_paiement'),
            mouvement_montant=F('montant'),
            type=Value('entree', output_field=CharField()),
            descri=F('note'),
            ref=F('facture__num_facture'),
            order_to=Concat(
                F('facture__client__nom'), Value(' '), F('facture__client__prenom'),
                output_field=CharField()
            ),
            entite_name=F('facture__entreprise__designation')
        )

    # ---- 2. Dépenses (Sorties en espèce) ----
    depenses = Depenses.objects.filter(mode_paiement='esp').values(
        nom=F('label'),
        date=F('date_paiement'),
        mouvement_montant=F('montant_ttc'),
        type=Value('sortie', output_field=CharField()),
        descr=F('description'),
        ref=F('piece'),
        order_to=F('fournisseur__designation'),
        entite_name=Value('ets', output_field=CharField())
    )

    # ---- 3. Fusion et tri chronologique ----
    mouvements = sorted(
        chain(paiements, autres_produits, consulting_paiements, depenses),
        key=lambda x: x['date'] or datetime.min
    )

    # ---- 4. Calcul du solde cumulatif ----
    solde = 0
    results = []
    for mv in mouvements:
        montant = float(mv['mouvement_montant']) if mv.get('mouvement_montant') else 0
        if mv['type'] == 'entree':
            solde += montant
        else:
            solde -= montant

        results.append({
            "date": mv['date'],
            "type": mv['type'],
            "nom": mv['nom'],
            "montant": montant,
            "solde": solde,
            "order_to": mv['order_to']
        })

    return JsonResponse({
        "status": "success",
        "solde_final": solde,
        "mouvements": results
    }, safe=False)


@login_required(login_url="institut_app:login")
def brouillard_banck_json(request):
    # Load t_conseil Paiement model
    try:
        ConseilPaiement = apps.get_model('t_conseil', 'Paiement')
    except (LookupError, ImportError):
        ConseilPaiement = None

    # ---- 1. Paiements (Entrées en banque) ----
    paiements = Paiements.objects.filter(mode_paiement__in=['vir', 'che']).values(
        nom=F('paiement_label'),
        date=F('date_paiement'),
        mouvement_montant=F('montant_paye'),
        type=Value('entree', output_field=CharField()),
        descri=Coalesce('paiement_label', Value('')),
        ref=F('num'),
        order_to=Concat(
            F('prospect__nom'), Value(' '), F('prospect__prenom'),
            output_field=CharField()
        ),
        entite_name=F('due_paiements__ref_echeancier__entite__designation'),
        mode=F('mode_paiement')
    )

    # ---- 1b. AutreProduit (Entrées en banque) ----
    autres_produits = AutreProduit.objects.filter(mode_paiement__in=['chq', 'vir']).values(
        nom=F('label'),
        date=F('date_paiement'),
        mouvement_montant=F('montant_paiement'),
        type=Value('entree', output_field=CharField()),
        descri=F('label'),
        ref=F('num'),
        order_to=Concat(
            F('client__nom'), Value(' '), F('client__prenom'),
            output_field=CharField()
        ),
        entite_name=F('entite__designation'),
        mode=F('mode_paiement')
    )

    # ---- 1c. Consulting Paiement (Entrées en banque) ----
    consulting_paiements = []
    if ConseilPaiement:
        consulting_paiements = ConseilPaiement.objects.filter(mode_paiement__in=['virement', 'cheque']).values(
            nom=Value('Paiement Facture', output_field=CharField()),
            date=F('date_paiement'),
            mouvement_montant=F('montant'),
            type=Value('entree', output_field=CharField()),
            descri=F('note'),
            ref=F('facture__num_facture'),
            order_to=Concat(
                F('facture__client__nom'), Value(' '), F('facture__client__prenom'),
                output_field=CharField()
            ),
            entite_name=F('facture__entreprise__designation'),
            mode=F('mode_paiement')
        )

    # ---- 2. Dépenses (Sorties en banque) ----
    depenses = Depenses.objects.filter(mode_paiement__in=['vir', 'che']).values(
        nom=F('label'),
        date=F('date_paiement'),
        mouvement_montant=F('montant_ttc'),
        type=Value('sortie', output_field=CharField()),
        descr=F('description'),
        ref=F('piece'),
        order_to=F('fournisseur__designation'),
        entite_name=Value('ets', output_field=CharField()),
        mode=F('mode_paiement')
    )

    # ---- 3. Fusion et tri chronologique ----
    mouvements = sorted(
        chain(paiements, autres_produits, consulting_paiements, depenses),
        key=lambda x: x['date'] or datetime.min
    )

    # ---- 4. Calcul du solde cumulatif ----
    solde = 0
    results = []
    for mv in mouvements:
        montant = float(mv['mouvement_montant']) if mv.get('mouvement_montant') else 0
        if mv['type'] == 'entree':
            solde += montant
        else:
            solde -= montant

        results.append({
            "date": mv['date'],
            "type": mv['type'],
            "nom": mv['nom'],
            "montant": montant,
            "solde": solde,
            "order_to": mv['order_to']
        })

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
            try:
                item = {
                    'id' : i.id,
                    'type' : i.get_operation_type_display(),
                    'montant' : float(i.montant),
                    'date_operation' : i.date_operation.strftime('%Y-%m-%d') if i.date_operation else None,
                    'is_approche' : i.is_rapproche,
                    'compte' : i.compte_bancaire.bank_name if i.compte_bancaire else None,
                }

                if i.paiement:
                    client_name = f"{i.paiement.prospect.nom} {i.paiement.prospect.prenom or ''}".strip() if i.paiement.prospect else "Client inconnu"
                    entite_name = "N/A"
                    if i.paiement.due_paiements:
                        if i.paiement.due_paiements.entite:
                            entite_name = i.paiement.due_paiements.entite.designation
                        elif i.paiement.due_paiements.ref_echeancier and i.paiement.due_paiements.ref_echeancier.entite:
                            entite_name = i.paiement.due_paiements.ref_echeancier.entite.designation

                    item.update({
                        'mode_paiement' : i.paiement.mode_paiement,
                        'label_mode_paiement' : i.paiement.get_mode_paiement_display(),
                        'paiement_id' : i.paiement.id,
                        'paiement_ref' : i.paiement.reference_paiement,
                        'client' : client_name,
                        'client_id' : i.paiement.prospect.id if i.paiement.prospect else None,
                        'entite' : entite_name,
                    })
                elif i.autre_produit:
                    client_name = "Anonyme"
                    if i.autre_produit.client:
                        client_name = f"{i.autre_produit.client.nom} {i.autre_produit.client.prenom or ''}".strip()
                    
                    item.update({
                        'mode_paiement' : i.autre_produit.mode_paiement,
                        'label_mode_paiement' : i.autre_produit.get_mode_paiement_display(),
                        'paiement_id' : i.autre_produit.id,
                        'paiement_ref' : i.autre_produit.reference or f"AUT-{i.autre_produit.id}",
                        'client' : client_name,
                        'client_id' : i.autre_produit.client.id if i.autre_produit.client else None,
                        'entite' : i.autre_produit.entite.designation if i.autre_produit.entite else "N/A",
                    })
                elif i.conseil_paiement:
                    client_name = "Client inconnu"
                    if i.conseil_paiement.facture and i.conseil_paiement.facture.client:
                        client_name = f"{i.conseil_paiement.facture.client.nom} {i.conseil_paiement.facture.client.prenom or ''}".strip()
                    
                    item.update({
                        'mode_paiement' : i.conseil_paiement.mode_paiement,
                        'label_mode_paiement' : i.conseil_paiement.get_mode_paiement_display(),
                        'paiement_id' : i.conseil_paiement.id,
                        'paiement_ref' : i.conseil_paiement.reference or f"INV-{i.conseil_paiement.id}",
                        'client' : client_name,
                        'client_id' : i.conseil_paiement.facture.client.id if i.conseil_paiement.facture and i.conseil_paiement.facture.client else None,
                        'entite' : i.conseil_paiement.facture.entreprise.designation if i.conseil_paiement.facture and i.conseil_paiement.facture.entreprise else "N/A",
                    })
                
                liste_paiements.append(item)
            except Exception as e:
                print(f"Error mapping operation {i.id}: {e}")
                continue

        for i in depenses:
            try:
                if i.depense:
                    liste_depenses.append({
                        'id' : i.id,
                        'fournisseur' : i.depense.fournisseur.designation if i.depense.fournisseur else "Divers",
                        'montant' : float(i.montant),
                        'categorie' : i.depense.category.name if i.depense.category else "Autre",
                        'date' : i.date_operation.strftime('%Y-%m-%d') if i.date_operation else None,
                        'statut' : "Validé" if i.depense.etat else "En attente",
                        'compte' : i.compte_bancaire.bank_name if i.compte_bancaire else None,
                        'entite' : i.depense.entite.designation if i.depense.entite else "N/A",
                    })
            except Exception as e:
                print(f"Error mapping expense {i.id}: {e}")
                continue

        data = {
            'paiements' : liste_paiements,
            'depenses'  : liste_depenses,
        }

    
        return JsonResponse(data, safe=False)

    else:
        return JsonResponse({"status" : "error"})
    
@login_required(login_url="institut_app:login")
def ApiImputeBankPaiment(request):
    if request.method == "POST":
        operationId = request.POST.get('operationId')
        compte = request.POST.get('compte')

        if not operationId or not compte:
            return JsonResponse({"status":"error","message":"Informations manquantes"})
        
        ## Imputation du paiement
        


    else:
        return JsonResponse({"status":"error",'message' : 'methode non autorise'})

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
