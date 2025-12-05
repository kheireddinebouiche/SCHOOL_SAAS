from django.shortcuts import render
from django.http import JsonResponse
from ..models import *
from django.db import transaction
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from itertools import chain
from datetime import datetime
from django.db.models import F, Value
from django.db.models.functions import Coalesce
from itertools import chain


@login_required(login_url="institut_app:login")
def PageBrouillardCaisse(request):
    return render(request, 'tenant_folder/comptabilite/caisse/brouillad_caisse.html')


@login_required(login_url="institut_app:login")
def brouillard_caisse_json(request):

    # ---- 1. Paiements (Entrées en espèce) ----
    paiements = Paiements.objects.filter(
        mode_paiement='esp',
    ).values(
        nom=F('paiement_label'),
        date=F('date_paiement'),
        montant=F('montant_paye'),
        type=Value('entree', output_field=models.CharField()),
        descri=Coalesce('paiement_label', Value('')),
        ref=F('num')
    )

    # ---- 2. Dépenses (Sorties en espèce) ----
    depenses = Depenses.objects.filter(
        mode_paiement='esp'
    ).values(
        nom =F('label'),
        date=F('date_paiement'),
        montant=F('montant_ttc'),
        type=Value('sortie', output_field=models.CharField()),
        descr=F('description'),
        ref=F('piece')
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
            "solde": solde
        })

    # ---- 5. Retour JSON propre ----
    return JsonResponse({
        "status": "success",
        "solde_final": solde,
        "mouvements": results
    }, safe=False)


def PaiementsData(request):
    paiements = Paiements.objects.filter(mode_paiement = 'esp') 