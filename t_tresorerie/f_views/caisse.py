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
from django.db.models import F, Value, CharField, Q, Case, When, Sum, Max
from django.db.models.functions import Coalesce
from django.db.models.functions import Concat
from django.contrib.humanize.templatetags.humanize import intcomma
import json
from django.views.decorators.http import require_POST
from t_crm.models import UserActionLog


@login_required(login_url="institut_app:login")
def PageBrouillardCaisse(request):
    today = datetime.now().date()
    default_year = today.year if today.month >= 8 else today.year - 1
    
    try:
        selected_year = int(request.GET.get('year', default_year))
    except ValueError:
        selected_year = default_year
        
    context = {
        'selected_year': selected_year,
        'available_years': range(2023, default_year + 2)
    }
    return render(request, 'tenant_folder/comptabilite/caisse/brouillad_caisse.html', context)

@login_required(login_url="institut_app:login")
def PageBrouillardBanque(request):
    today = datetime.now().date()
    default_year = today.year if today.month >= 8 else today.year - 1
    
    try:
        selected_year = int(request.GET.get('year', default_year))
    except ValueError:
        selected_year = default_year
        
    context = {
        'selected_year': selected_year,
        'available_years': range(2023, default_year + 2)
    }
    return render(request,'tenant_folder/comptabilite/caisse/brouillard_banque.html', context)

@login_required(login_url="institut_app:login")
def brouillard_caisse_json(request):
    # Load t_conseil Paiement model
    try:
        ConseilPaiement = apps.get_model('t_conseil', 'Paiement')
    except (LookupError, ImportError):
        ConseilPaiement = None

    # Fiscal Year Filtering
    today = datetime.now().date()
    default_year = today.year if today.month >= 8 else today.year - 1
    try:
        year = int(request.GET.get('year', default_year))
    except ValueError:
        year = default_year
        
    start_date = datetime(year, 8, 1).date()
    end_date = datetime(year + 1, 7, 31).date()

    # ---- 1. Paiements (Entrées en espèce) ----
    paiements = Paiements.objects.filter(mode_paiement='esp', date_paiement__gte=start_date, date_paiement__lte=end_date).exclude(date_paiement__isnull=True).values(
        nom=F('paiement_label'),
        date=F('date_paiement'),
        mouvement_montant=Coalesce(F('montant_paye'), Value(0, output_field=models.DecimalField())),
        type=Value('entree', output_field=CharField()),
        descri=Coalesce('paiement_label', Value('')),
        ref=F('num'),
        order_to=Concat(
            F('prospect__nom'), Value(' '), F('prospect__prenom'),
            output_field=CharField()
        ),
        entite_name=F('entite__designation'),
        mapped_entite_id=F('entite__id')
    )

    # ---- 1b. AutreProduit (Entrées en espèce) ----
    autres_produits = AutreProduit.objects.filter(mode_paiement='esp', date_paiement__gte=start_date, date_paiement__lte=end_date).exclude(date_paiement__isnull=True).values(
        nom=F('label'),
        date=F('date_paiement'),
        mouvement_montant=Coalesce(F('montant_paiement'), Value(0, output_field=models.DecimalField())),
        type=Value('entree', output_field=CharField()),
        descri=F('label'),
        ref=F('num'),
        order_to=Concat(
            F('client__nom'), Value(' '), F('client__prenom'),
            output_field=CharField()
        ),
        entite_name=F('entite__designation'),
        mapped_entite_id=F('entite__id')
    )

    # ---- 1c. Consulting Paiement (Entrées en espèce) ----
    consulting_paiements = []
    if ConseilPaiement:
        consulting_paiements = ConseilPaiement.objects.filter(mode_paiement='esp', date_paiement__gte=start_date, date_paiement__lte=end_date).exclude(date_paiement__isnull=True).values(
            nom=Value('Paiement Facture', output_field=CharField()),
            date=F('date_paiement'),
            mouvement_montant=Coalesce(F('montant'), Value(0, output_field=models.DecimalField())),
            type=Value('entree', output_field=CharField()),
            descri=F('note'),
            ref=F('facture__num_facture'),
            order_to=Concat(
                F('facture__client__nom'), Value(' '), F('facture__client__prenom'),
                output_field=CharField()
            ),
            entite_name=F('facture__entreprise__designation'),
            mapped_entite_id=F('facture__entreprise__id')
        )

    # ---- 2. Dépenses (Sorties en espèce) ----
    depenses = Depenses.objects.filter(mode_paiement='esp', date_paiement__gte=start_date, date_paiement__lte=end_date).order_by('date_paiement').exclude(date_paiement__isnull=True).values(
        nom=F('label'),
        date=F('date_paiement'),
        mouvement_montant=Coalesce(F('montant_ttc'), F('montant_ht'), Value(0, output_field=models.DecimalField())),
        type=Value('sortie', output_field=CharField()),
        descr=F('description'),
        ref=Coalesce('reference', Value('')),
        order_to=Case(
            When(fournisseur__isnull=False, then=F('fournisseur__designation')),
            When(client__isnull=False, then=Concat(F('client__nom'), Value(' '), F('client__prenom'))),
            default=Value('Inconnu'),
            output_field=CharField()
        ),
        entite_name=F('entite__designation'),
        mapped_entite_id=F('entite__id')
    )

    # ---- 2b. Dépôts en Banque (Sorties de caisse) ----
    depots_banque = DepotBanque.objects.filter(date_depot__gte=start_date, date_depot__lte=end_date).values(
        nom=Value('Dépôt en Banque', output_field=CharField()),
        date=F('date_depot'),
        mouvement_montant=Coalesce(F('montant'), Value(0, output_field=models.DecimalField())),
        type=Value('sortie', output_field=CharField()),
        descri=F('observation'),
        ref=F('num'),
        order_to=F('agent_remettant'),
        entite_name=F('entite__designation'),
        mapped_entite_id=F('entite__id')
    )

    # ---- 3. Fusion et tri chronologique ----
    mouvements = sorted(
        chain(paiements, autres_produits, consulting_paiements, depenses, depots_banque),
        key=lambda x: (
            x['date'] if isinstance(x['date'], datetime) 
            else datetime.combine(x['date'], datetime.min.time())
        ) if x['date'] else datetime.min
    )

    # ---- 4. Calcul du solde cumulatif ----
    entite_filter = request.GET.get('entite', '0')
    solde_initial_obj = None
    if entite_filter != '0':
        solde_initial_obj = SoldeInitial.objects.filter(type='caisse', annee_scolaire=year, entite_id=entite_filter).first()
    else:
        solde_initial_obj = SoldeInitial.objects.filter(type='caisse', annee_scolaire=year, entite__isnull=True).first()
    
    initial_amount = float(solde_initial_obj.montant) if solde_initial_obj else 0.0
    solde = initial_amount
    results = []
    for mv in mouvements:
        montant = float(mv['mouvement_montant'] or 0)
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
            "order_to": mv['order_to'],
            "entite_name": mv.get('entite_name'),
            "entite_id": mv.get('mapped_entite_id')
        })

    return JsonResponse({
        "status": "success",
        "solde_initial": initial_amount,
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

    # Fiscal Year Filtering
    today = datetime.now().date()
    default_year = today.year if today.month >= 8 else today.year - 1
    try:
        year = int(request.GET.get('year', default_year))
    except ValueError:
        year = default_year
        
    start_date = datetime(year, 8, 1).date()
    end_date = datetime(year + 1, 7, 31).date()

    # Fetch Solde Initial for the selected year/entity
    entite_filter = request.GET.get('entite', '0')
    solde_initial_obj = None
    if entite_filter != '0':
        solde_initial_obj = SoldeInitial.objects.filter(type='banque', annee_scolaire=year, entite_id=entite_filter).first()
    else:
        solde_initial_obj = SoldeInitial.objects.filter(type='banque', annee_scolaire=year, entite__isnull=True).first()
    
    initial_amount = float(solde_initial_obj.montant) if solde_initial_obj else 0.0

    # ---- 1. Paiements (Entrées en banque) ----
    paiements = Paiements.objects.filter(mode_paiement__in=['vir', 'che'], date_paiement__gte=start_date, date_paiement__lte=end_date, is_done=True).exclude(date_paiement__isnull=True).values(
        nom=F('paiement_label'),
        date=F('date_paiement'),
        mouvement_montant=Coalesce(F('montant_paye'), Value(0, output_field=models.DecimalField())),
        type=Value('entree', output_field=CharField()),
        descri=Coalesce('paiement_label', Value('')),
        ref=F('num'),
        order_to=Concat(
            F('prospect__nom'), Value(' '), F('prospect__prenom'),
            output_field=CharField()
        ),
        entite_name=F('entite__designation'),
        mapped_entite_id=F('entite__id'),
        mode=F('mode_paiement'),
        reference=F('reference_paiement')
    )

    # ---- 1b. AutreProduit (Entrées en banque) ----
    autres_produits = AutreProduit.objects.filter(mode_paiement__in=['che', 'vir'], date_paiement__gte=start_date, date_paiement__lte=end_date, is_done=True).exclude(date_paiement__isnull=True).values(
        'reference',
        nom=F('label'),
        date=F('date_paiement'),
        mouvement_montant=Coalesce(F('montant_paiement'), Value(0, output_field=models.DecimalField())),
        type=Value('entree', output_field=CharField()),
        descri=F('label'),
        ref=F('num'),
        order_to=Concat(
            F('client__nom'), Value(' '), F('client__prenom'),
            output_field=CharField()
        ),
        entite_name=F('entite__designation'),
        mapped_entite_id=F('entite__id'),
        mode=F('mode_paiement')
    )

    # ---- 1c. Consulting Paiement (Entrées en banque) ----
    consulting_paiements = []
    if ConseilPaiement:
        consulting_paiements = ConseilPaiement.objects.filter(mode_paiement__in=['vir', 'che'], date_paiement__gte=start_date, date_paiement__lte=end_date, is_done=True).exclude(date_paiement__isnull=True).values(
            'reference',
            nom=Value('Paiement Facture', output_field=CharField()),
            date=F('date_paiement'),
            mouvement_montant=Coalesce(F('montant'), Value(0, output_field=models.DecimalField())),
            type=Value('entree', output_field=CharField()),
            descri=F('note'),
            ref=F('facture__num_facture'),
            order_to=Concat(
                F('facture__client__nom'), Value(' '), F('facture__client__prenom'),
                output_field=CharField()
            ),
            entite_name=F('facture__entreprise__designation'),
            mapped_entite_id=F('facture__entreprise__id'),
            mode=F('mode_paiement')
        )

    # ---- 2. Dépenses (Sorties en banque) ----
    depenses = Depenses.objects.filter(mode_paiement__in=['vir', 'che'], date_paiement__gte=start_date, date_paiement__lte=end_date, etat=True).order_by('date_paiement').exclude(date_paiement__isnull=True).values(
        'reference',
        nom=F('label'),
        date=F('date_paiement'),
        mouvement_montant=Coalesce(F('montant_ttc'), F('montant_ht'), Value(0, output_field=models.DecimalField())),
        type=Value('sortie', output_field=CharField()),
        descr=F('description'),
        ref=Coalesce('reference', Value('')),
        order_to=Case(
            When(fournisseur__isnull=False, then=F('fournisseur__designation')),
            When(client__isnull=False, then=Concat(F('client__nom'), Value(' '), F('client__prenom'))),
            default=Value('Inconnu'),
            output_field=CharField()
        ),
        entite_name=F('entite__designation'),
        mapped_entite_id=F('entite__id'),
        mode=F('mode_paiement')
    )

    # ---- 2b. Dépôts en Banque (Entrées) ----
    depots_banque = DepotBanque.objects.filter(date_depot__gte=start_date, date_depot__lte=end_date).values(
        nom=Value('Dépôt en Banque', output_field=CharField()),
        date=F('date_depot'),
        mouvement_montant=Coalesce(F('montant'), Value(0, output_field=models.DecimalField())),
        type=Value('entree', output_field=CharField()),
        descr=F('observation'),
        ref=F('num'),
        order_to=F('agent_remettant'),
        entite_name=F('entite__designation'),
        mapped_entite_id=F('entite__id'),
        mode=Value('esp', output_field=CharField()),
        reference=F('reference_bordereau')
    )

    # ---- 3. Fusion et tri chronologique ----
    mouvements = sorted(
        chain(paiements, autres_produits, consulting_paiements, depenses, depots_banque),
        key=lambda x: x['date'] or datetime.min
    )

    # ---- 4. Calcul du solde cumulatif ----
    solde = initial_amount
    results = []
    for mv in mouvements:
        montant = float(mv['mouvement_montant'] or 0)
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
            "order_to": mv['order_to'],
            "entite_name": mv.get('entite_name'),
            "entite_id": mv.get('mapped_entite_id'),
            "ref": mv.get('ref'),
            "mode": mv.get('mode'),
            "reference": mv.get('reference')
        })

    return JsonResponse({
        "status": "success",
        "solde_initial": initial_amount,
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
        paiements = OperationsBancaire.objects.filter(operation_type="entree")
        depenses = OperationsBancaire.objects.filter(operation_type="sortie")

        liste_paiements = []
        liste_depenses  = []

        for i in paiements:
            try:
                item = {
                    'id' : i.id,
                    'type' : i.get_operation_type_display(),
                    'montant' : float(i.montant),
                    'date' : i.date_operation.strftime('%Y-%m-%d') if i.date_operation else None,
                    'is_rapproche' : i.is_rapproche,
                    'compte' : i.compte_bancaire.bank_name if i.compte_bancaire else None,
                }

                if i.paiement:
                    client_name = "Client inconnu"
                    if i.paiement.prospect:
                        client_name = f"{i.paiement.prospect.nom or ''} {i.paiement.prospect.prenom or ''}".strip() or "Client inconnu"
                    
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
                        'date_creation' : i.paiement.created_at.strftime('%Y-%m-%d') if i.paiement.created_at else None,
                        'date_effective' : i.paiement.date_paiement.strftime('%Y-%m-%d') if i.paiement.date_paiement else None,
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
                        'date_creation' : i.autre_produit.date_operation.strftime('%Y-%m-%d') if i.autre_produit.date_operation else None,
                        'date_effective' : i.autre_produit.date_paiement.strftime('%Y-%m-%d') if i.autre_produit.date_paiement else None,
                    })
                elif i.conseil_paiement:
                    client_name = "Client inconnu"
                    if i.conseil_paiement.facture and i.conseil_paiement.facture.client:
                        client_name = f"{i.conseil_paiement.facture.client.nom or ''} {i.conseil_paiement.facture.client.prenom or ''}".strip() or "Client inconnu"
                    
                    item.update({
                        'mode_paiement' : i.conseil_paiement.mode_paiement,
                        'label_mode_paiement' : i.conseil_paiement.get_mode_paiement_display(),
                        'paiement_id' : i.conseil_paiement.id,
                        'paiement_ref' : i.conseil_paiement.reference or f"INV-{i.conseil_paiement.id}",
                        'client' : client_name,
                        'client_id' : i.conseil_paiement.facture.client.id if i.conseil_paiement.facture and i.conseil_paiement.facture.client else None,
                        'entite' : i.conseil_paiement.facture.entreprise.designation if i.conseil_paiement.facture and i.conseil_paiement.facture.entreprise else "N/A",
                        'date_creation' : i.conseil_paiement.created_at.strftime('%Y-%m-%d') if i.conseil_paiement.created_at else None,
                        'date_effective' : i.conseil_paiement.date_paiement.strftime('%Y-%m-%d') if i.conseil_paiement.date_paiement else None,
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
                        'fournisseur' : i.depense.fournisseur.designation if i.depense.fournisseur else (f"{i.depense.client.nom} {i.depense.client.prenom or ''}".strip() if i.depense.client else "Divers"),
                        'montant' : float(i.montant),
                        'categorie' : i.depense.category.name if i.depense.category else "Autre",
                        'date' : i.date_operation.strftime('%Y-%m-%d') if i.date_operation else None,
                        'statut' : "Validé" if i.depense.etat else "En attente",
                        'compte' : i.compte_bancaire.bank_name if i.compte_bancaire else None,
                        'entite' : i.depense.entite.designation if i.depense.entite else "N/A",
                        'mode_paiement' : i.depense.mode_paiement,
                        'is_rapproche' : i.is_rapproche,
                        'date_creation' : i.depense.created_at.strftime('%Y-%m-%d') if i.depense.created_at else None,
                        'date_effective' : i.depense.date_paiement.strftime('%Y-%m-%d') if i.depense.date_paiement else None,
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
        compte_id = request.POST.get('compte')
        date_valeur = request.POST.get('date_valeur')

        if not operationId or not compte_id:
            return JsonResponse({"status":"error","message":"Informations manquantes"})
        
        try:
            with transaction.atomic():
                operation = OperationsBancaire.objects.get(id=operationId)
                compte = BankAccount.objects.get(id=compte_id)
                
                operation.compte_bancaire = compte
                operation.is_rapproche = True
                operation.is_paid = True
                if date_valeur:
                    operation.date_paiement = date_valeur
                else:
                    operation.date_paiement = datetime.now().date()
                
                operation.save()
                
                UserActionLog.objects.create(
                    user=request.user,
                    action_type='UPDATE',
                    target_model='OperationsBancaire',
                    target_id=str(operationId),
                    details=f"Imputation bancaire de l'opération {operation.reference_bancaire or operationId} sur le compte {compte.bank_name}. Montant: {operation.montant} DA.",
                    ip_address=request.META.get('REMOTE_ADDR')
                )

                return JsonResponse({
                    "status": "success", 
                    "message": "Opération rapprochée avec succès"
                })
        except OperationsBancaire.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Opération introuvable"})
        except BankAccount.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Compte bancaire introuvable"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})

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
        try:
            obj=OperationsBancaire.objects.get(id = id)
            
            client_name = "N/A"
            fournisseur_name = "N/A"
            email = "N/A"
            phone = "N/A"
            categorie = "N/A"
            mode_paiement_label = "N/A"
            compte_name = obj.compte_bancaire.bank_name if obj.compte_bancaire else "N/A"
            observations = obj.justification or "Aucune observation"
            
            if obj.paiement:
                if obj.paiement.prospect:
                    client_name = f"{obj.paiement.prospect.nom or ''} {obj.paiement.prospect.prenom or ''}".strip()
                    email = obj.paiement.prospect.email or "N/A"
                    phone = getattr(obj.paiement.prospect, 'telephone', "N/A") or getattr(obj.paiement.prospect, 'phone', "N/A")
                mode_paiement_label = obj.paiement.get_mode_paiement_display()
            elif obj.autre_produit:
                if obj.autre_produit.client:
                    client_name = f"{obj.autre_produit.client.nom or ''} {obj.autre_produit.client.prenom or ''}".strip()
                    email = obj.autre_produit.client.email or "N/A"
                    phone = getattr(obj.autre_produit.client, 'telephone', "N/A") or getattr(obj.autre_produit.client, 'phone', "N/A")
                mode_paiement_label = obj.autre_produit.get_mode_paiement_display()
            elif obj.conseil_paiement:
                if obj.conseil_paiement.facture and obj.conseil_paiement.facture.client:
                    client_name = f"{obj.conseil_paiement.facture.client.nom or ''} {obj.conseil_paiement.facture.client.prenom or ''}".strip()
                    email = obj.conseil_paiement.facture.client.email or "N/A"
                    phone = getattr(obj.conseil_paiement.facture.client, 'telephone', "N/A") or getattr(obj.conseil_paiement.facture.client, 'phone', "N/A")
                mode_paiement_label = obj.conseil_paiement.get_mode_paiement_display()
            elif obj.depense:
                if obj.depense.fournisseur:
                    fournisseur_name = obj.depense.fournisseur.designation
                    email = getattr(obj.depense.fournisseur, 'email', "N/A") or "N/A"
                    phone = getattr(obj.depense.fournisseur, 'telephone', "N/A") or getattr(obj.depense.fournisseur, 'phone', "N/A")
                elif obj.depense.client:
                    fournisseur_name = f"{obj.depense.client.nom or ''} {obj.depense.client.prenom or ''}".strip()
                    email = obj.depense.client.email or "N/A"
                    phone = getattr(obj.depense.client, 'telephone', "N/A") or getattr(obj.depense.client, 'phone', "N/A")
                if obj.depense.category:
                    categorie = obj.depense.category.name
                mode_paiement_label = obj.depense.get_mode_paiement_display()
                observations = obj.depense.description or observations
            
            data = {
                'id' : obj.id,
                'operation_type' : obj.get_operation_type_display(),
                'type_code' : obj.operation_type,
                'montant' : float(obj.montant) if obj.montant else 0,
                'date_operation' : obj.date_operation.strftime('%Y-%m-%d') if obj.date_operation else None,
                'reference_bancaire' : obj.reference_bancaire if obj.reference_bancaire else None,
                'is_rapproche' : obj.is_rapproche,
                'is_paid' : obj.is_paid,
                'date_paiement' : obj.date_paiement.strftime('%Y-%m-%d') if obj.date_paiement else None,
                'client_name': client_name,
                'fournisseur_name': fournisseur_name,
                'email': email,
                'phone': str(phone),
                'categorie': categorie,
                'mode_paiement_label': mode_paiement_label,
                'compte_name': compte_name,
                'observations': observations,
            }
            return JsonResponse(data, safe=False)
        except Exception as e:
            return JsonResponse({"status" : "error", "message": str(e)})

    else:
        return JsonResponse({"status" : "error"})


@login_required(login_url="institut_app:login")
@ajax_required
def ApiListBankAccount(request):
    if request.method == "GET":
        liste = BankAccount.objects.all().values('id','entreprise__designation','bank_name','bank_code')
        return JsonResponse(list(liste), safe=False)
    else:
        return JsonResponse({"status": "error"})

@login_required(login_url="institut_app:login")
def PageRecouvrement(request):
    return render(request, 'tenant_folder/comptabilite/caisse/recouvrement_paiement.html')

@login_required(login_url="institut_app:login")
def ApiUpdateEffectiveDate(request):
    if request.method == "POST":
        paiement_id = request.POST.get('paiement_id')
        effective_date = request.POST.get('effective_date')
        p_type = request.POST.get('type', 'standard')

        if not paiement_id or not effective_date:
            return JsonResponse({"status": "error", "message": "Informations manquantes"})

        try:
            from t_tresorerie.models import OperationsBancaire
            
            if p_type == 'standard':
                paiement = Paiements.objects.get(id=paiement_id)
                paiement.date_paiement = effective_date
                paiement.is_done = True
                paiement.save()
                OperationsBancaire.objects.filter(paiement=paiement).update(date_operation=effective_date)
            elif p_type == 'autre':
                paiement = AutreProduit.objects.get(id=paiement_id)
                paiement.date_paiement = effective_date
                paiement.is_done = True
                paiement.save()
                OperationsBancaire.objects.filter(autre_produit=paiement).update(date_operation=effective_date)
            elif p_type == 'conseil':
                from t_conseil.models import Paiement as ConseilPaiement
                paiement = ConseilPaiement.objects.get(id=paiement_id)
                paiement.date_paiement = effective_date
                paiement.is_done = True
                paiement.save()
                OperationsBancaire.objects.filter(conseil_paiement=paiement).update(date_operation=effective_date)
            else:
                return JsonResponse({"status": "error", "message": "Type de paiement invalide"})

            return JsonResponse({"status": "success", "message": "Date effective mise à jour avec succès"})
        except (Paiements.DoesNotExist, AutreProduit.DoesNotExist, Exception) as e:
            return JsonResponse({"status": "error", "message": str(e)})
    return JsonResponse({"status": "error", "message": "Méthode non autorisée"})

@login_required(login_url="institut_app:login")
def ApiListRecouvrementPaiements(request):
    if request.method == "GET":
        data = []
        
        # 1. Standard Payments
        paiements = Paiements.objects.filter(
            mode_paiement__in=['che', 'vir'],
            is_done=False
        ).select_related('prospect', 'due_paiements__entite')

        for p in paiements:
            client_name = "Client inconnu"
            if p.prospect:
                client_name = f"{p.prospect.nom or ''} {p.prospect.prenom or ''}".strip() or "Client inconnu"
            
            entite_name = "N/A"
            if p.due_paiements:
                if p.due_paiements.entite:
                    entite_name = p.due_paiements.entite.designation
                elif p.due_paiements.ref_echeancier and p.due_paiements.ref_echeancier.entite:
                    entite_name = p.due_paiements.ref_echeancier.entite.designation

            data.append({
                'id': p.id,
                'type': 'standard',
                'num': p.num,
                'client': client_name,
                'montant': float(p.montant_paye) if p.montant_paye else 0,
                'mode_paiement': p.get_mode_paiement_display(),
                'date_paiement': p.date_paiement.strftime('%Y-%m-%d') if p.date_paiement else None,
                'reference': p.reference_paiement or '-',
                'entite': entite_name,
                'created_at': p.created_at.strftime('%Y-%m-%d') if p.created_at else None,
            })

        # 2. AutreProduit Payments
        autres = AutreProduit.objects.filter(
            mode_paiement__in=['che', 'vir'],
            is_done=False
        ).select_related('client', 'entite')
        
        for a in autres:
            client_name = "Client inconnu"
            if a.client:
                client_name = f"{a.client.nom or ''} {a.client.prenom or ''}".strip() or "Client inconnu"
                
            data.append({
                'id': a.id,
                'type': 'autre',
                'num': a.num or f"AUT-{a.id}",
                'client': client_name,
                'montant': float(a.montant_paiement) if a.montant_paiement else 0,
                'mode_paiement': a.get_mode_paiement_display(),
                'date_paiement': a.date_paiement.strftime('%Y-%m-%d') if a.date_paiement else None,
                'reference': a.reference or '-',
                'entite': a.entite.designation if a.entite else 'N/A',
                'created_at': a.date_operation.strftime('%Y-%m-%d') if a.date_operation else None,
            })

        # 3. Conseil Payments
        from t_conseil.models import Paiement as ConseilPaiement
        conseil_p = ConseilPaiement.objects.filter(
            mode_paiement__in=['che', 'vir'],
            is_done=False
        ).select_related('facture__client', 'facture__entreprise')

        for cp in conseil_p:
            client_name = "Client inconnu"
            if cp.facture and cp.facture.client:
                client_name = f"{cp.facture.client.nom or ''} {cp.facture.client.prenom or ''}".strip() or "Client inconnu"

            data.append({
                'id': cp.id,
                'type': 'conseil',
                'num': cp.facture.num_facture if cp.facture else f"CON-{cp.id}",
                'client': client_name,
                'montant': float(cp.montant) if cp.montant else 0,
                'mode_paiement': cp.get_mode_paiement_display(),
                'date_paiement': cp.date_paiement.strftime('%Y-%m-%d') if cp.date_paiement else None,
                'reference': cp.reference or '-',
                'entite': cp.facture.entreprise.designation if cp.facture and cp.facture.entreprise else 'N/A',
                'created_at': cp.created_at.strftime('%Y-%m-%d') if cp.created_at else None,
            })
        
        return JsonResponse(data, safe=False)
    return JsonResponse({"status": "error", "message": "Méthode non autorisée"})

@login_required(login_url="institut_app:login")
def ApiRecouvrementStats(request):
    if request.method == "GET":
        # 1. Standard Payments
        paiements = Paiements.objects.filter(
            mode_paiement__in=['che', 'vir'],
            is_done=False
        )
        
        # 2. AutreProduit
        autres = AutreProduit.objects.filter(
            mode_paiement__in=['che', 'vir'],
            is_done=False
        )

        # 3. Conseil
        from t_conseil.models import Paiement as ConseilPaiement
        conseils = ConseilPaiement.objects.filter(
            mode_paiement__in=['che', 'vir'],
            is_done=False
        )

        # Aggregation
        total_montant = (sum(p.montant_paye for p in paiements if p.montant_paye) or 0) + \
                        (sum(a.montant_paiement for a in autres if a.montant_paiement) or 0) + \
                        (sum(c.montant for c in conseils if c.montant) or 0)
        
        total_count = paiements.count() + autres.count() + conseils.count()
        
        # Breakdown by mode
        total_cheques = (sum(p.montant_paye for p in paiements if p.mode_paiement == 'che') or 0) + \
                        (sum(a.montant_paiement for a in autres if a.mode_paiement == 'che') or 0) + \
                        (sum(c.montant for c in conseils if c.mode_paiement == 'che') or 0)
        
        total_virements = (sum(p.montant_paye for p in paiements if p.mode_paiement == 'vir') or 0) + \
                         (sum(a.montant_paiement for a in autres if a.mode_paiement == 'vir') or 0) + \
                         (sum(c.montant for c in conseils if c.mode_paiement == 'vir') or 0)

        data = {
            'total_montant': float(total_montant),
            'total_count': total_count,
            'total_cheques': float(total_cheques),
            'total_virements': float(total_virements),
        }
        return JsonResponse(data)
    return JsonResponse({"status": "error", "message": "Méthode non autorisée"})

@require_POST
@login_required(login_url="institut_app:login")
def api_set_solde_initial(request):
    try:
        data = json.loads(request.body)
        montant = data.get('montant')
        annee = data.get('annee')
        entite_id = data.get('entite_id')
        solde_type = data.get('type', 'caisse')

        if not annee:
            return JsonResponse({"status": "error", "message": "Année manquante"}, status=400)

        # Si entite_id est '0' ou vide, on considère le solde global (entite=None)
        entite = None
        if entite_id and entite_id != '0':
            entite = Entreprise.objects.get(id=entite_id)

        solde_obj, created = SoldeInitial.objects.update_or_create(
            type=solde_type,
            annee_scolaire=annee,
            entite=entite,
            defaults={'montant': montant}
        )

        UserActionLog.objects.create(
            user=request.user,
            action_type='UPDATE',
            target_model='SoldeInitial',
            target_id=str(solde_obj.id),
            details=f"Définition du solde initial ({solde_type}) pour l'année {annee} sur l'entité {entite.designation if entite else 'Global'}. Montant: {montant} DA.",
            ip_address=request.META.get('REMOTE_ADDR')
        )

        return JsonResponse({
            "status": "success", 
            "message": "Solde initial enregistré avec succès",
            "montant": float(solde_obj.montant)
        })
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)

@login_required(login_url="institut_app:login")
def api_list_soldes_initiaux(request):
    soldes = SoldeInitial.objects.all().order_by('-annee_scolaire', 'type')
    data = []
    for s in soldes:
        data.append({
            'id': s.id,
            'type': s.type,
            'type_label': s.get_type_display(),
            'montant': float(s.montant),
            'annee_scolaire': s.annee_scolaire,
            'annee_label': f"{s.annee_scolaire}/{s.annee_scolaire+1}",
            'entite_id': s.entite.id if s.entite else 0,
            'entite_name': s.entite.designation if s.entite else "Toutes les entités"
        })
    return JsonResponse(data, safe=False)

@login_required(login_url="institut_app:login")
def PageDepotBanque(request):
    return render(request, 'tenant_folder/comptabilite/caisse/depot_banque.html')

@login_required(login_url="institut_app:login")
def api_list_depots_banque(request):
    depots = DepotBanque.objects.all().order_by('-date_depot', '-created_at')
    
    # Filtering logic
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    entite_id = request.GET.get('entite_id')
    search = request.GET.get('search')

    if start_date:
        depots = depots.filter(date_depot__gte=start_date)
    if end_date:
        depots = depots.filter(date_depot__lte=end_date)
    if entite_id:
        depots = depots.filter(entite_id=entite_id)
    if search:
        depots = depots.filter(
            Q(num__icontains=search) | 
            Q(agent_remettant__icontains=search) | 
            Q(reference_bordereau__icontains=search)
        )

    data = []
    for d in depots:
        data.append({
            'id': d.id,
            'num': d.num,
            'date': d.date_depot.strftime('%Y-%m-%d'),
            'montant': float(d.montant),
            'entite': d.entite.designation,
            'agent': d.agent_remettant,
            'banque': d.banque_destinatrice.bank_name if d.banque_destinatrice else "Non spécifiée",
            'reference': d.reference_bordereau or "-",
            'observation': d.observation or ""
        })
    return JsonResponse(data, safe=False)

@require_POST
@login_required(login_url="institut_app:login")
def api_create_depot_banque(request):
    try:
        data = json.loads(request.body)
        
        # Validation de la date
        date_str = data.get('date')
        if date_str:
            try:
                date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                date_obj = datetime.now().date()
        else:
            date_obj = datetime.now().date()

        depot = DepotBanque.objects.create(
            date_depot=date_obj,
            montant=Decimal(str(data.get('montant') or 0)),
            entite_id=data.get('entite_id'),
            agent_remettant=data.get('agent'),
            banque_destinatrice_id=data.get('banque_id') if data.get('banque_id') and data.get('banque_id') != '0' else None,
            reference_bordereau=data.get('reference'),
            observation=data.get('observation'),
            cree_par=request.user
        )

        UserActionLog.objects.create(
            user=request.user,
            action_type='CREATE',
            target_model='DepotBanque',
            target_id=str(depot.id),
            details=f"Création d'un dépôt en banque (N°: {depot.num}) d'un montant de {depot.montant} DA par {depot.agent_remettant}.",
            ip_address=request.META.get('REMOTE_ADDR')
        )

        return JsonResponse({
            "status": "success", 
            "message": "Dépôt enregistré avec succès",
            "id": depot.id
        })
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)

@login_required(login_url="institut_app:login")
def imprimer_remise_fonds(request, pk):
    depot = DepotBanque.objects.get(pk=pk)
    context = {
        'depot': depot,
        'today': datetime.now(),
    }
    return render(request, 'tenant_folder/comptabilite/caisse/remise_fonds_pdf.html', context)

@login_required(login_url="institut_app:login")
def ApiLoadEntrepises(request):
    entreprises = Entreprise.objects.all().values('id', 'designation')
    return JsonResponse(list(entreprises), safe=False)

@login_required(login_url="institut_app:login")
def ApiListBankAccount(request):
    entreprise_id = request.GET.get('entreprise_id')
    banks = BankAccount.objects.all()
    if entreprise_id:
        banks = banks.filter(entreprise_id=entreprise_id)
    
    data = list(banks.values('id', 'bank_name', 'bank_code', 'bank_iban', 'entreprise__designation'))
    return JsonResponse(data, safe=False)
@login_required(login_url="institut_app:login")
def PageSituationComptes(request):
    bank_accounts = BankAccount.objects.filter(is_archived=False)
    situations = []
    
    total_general = Decimal('0.00')
    
    # Année scolaire actuelle
    today = datetime.now()
    current_year = today.year if today.month >= 8 else today.year - 1
    
    for account in bank_accounts:
        # 1. Solde Initial
        solde_init_obj = SoldeInitial.objects.filter(
            type='banque', 
            entite=account.entreprise,
            annee_scolaire=current_year
        ).first()
        
        solde_initial = solde_init_obj.montant if solde_init_obj else Decimal('0.00')
        
        # 2. Total Entrées (OperationsBancaire)
        entrees_op = OperationsBancaire.objects.filter(
            compte_bancaire=account,
            operation_type='entree'
        ).aggregate(total=Sum('montant'))['total'] or Decimal('0.00')
        
        # 3. Total Sorties (OperationsBancaire)
        sorties_op = OperationsBancaire.objects.filter(
            compte_bancaire=account,
            operation_type='sortie'
        ).aggregate(total=Sum('montant'))['total'] or Decimal('0.00')
        
        # 4. Total Dépôts (Depuis la caisse)
        depots = DepotBanque.objects.filter(
            banque_destinatrice=account
        ).aggregate(total=Sum('montant'))['total'] or Decimal('0.00')
        
        # Calcul Final
        total_entrees = entrees_op + depots
        total_sorties = sorties_op
        solde_actuel = solde_initial + total_entrees - total_sorties
        
        situations.append({
            'account': account,
            'solde_initial': solde_initial,
            'total_entrees': total_entrees,
            'total_sorties': total_sorties,
            'solde_actuel': solde_actuel,
        })
        
        total_general += solde_actuel

    context = {
        'situations': situations,
        'total_general': total_general,
        'current_year': f"{current_year}/{current_year+1}",
    }
    return render(request, 'tenant_folder/comptabilite/caisse/situation_comptes.html', context)

@login_required(login_url="institut_app:login")
def api_get_depot_banque(request, pk):
    try:
        depot = DepotBanque.objects.get(pk=pk)
        return JsonResponse({
            "status": "success",
            "data": {
                "id": depot.id,
                "entite_id": depot.entite.id,
                "banque_id": depot.banque_destinatrice.id if depot.banque_destinatrice else None,
                "date": depot.date_depot.strftime('%Y-%m-%d'),
                "montant": float(depot.montant),
                "agent": depot.agent_remettant,
                "reference": depot.reference_bordereau,
                "observation": depot.observation
            }
        })
    except DepotBanque.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Dépôt non trouvé"}, status=404)

@login_required(login_url="institut_app:login")
@require_POST
def api_update_depot_banque(request, pk):
    try:
        depot = DepotBanque.objects.get(pk=pk)
        data = json.loads(request.body)
        
        # Validation de la date
        date_str = data.get('date')
        if date_str:
            try:
                date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
                depot.date_depot = date_obj
            except ValueError:
                pass

        depot.montant = Decimal(str(data.get('montant') or 0))
        depot.entite_id = data.get('entite_id')
        depot.agent_remettant = data.get('agent')
        depot.banque_destinatrice_id = data.get('banque_id') if data.get('banque_id') and data.get('banque_id') != '0' else None
        depot.reference_bordereau = data.get('reference')
        depot.observation = data.get('observation')
        
        depot.save()
        
        UserActionLog.objects.create(
            user=request.user,
            action_type='UPDATE',
            target_model='DepotBanque',
            target_id=str(pk),
            details=f"Mise à jour du dépôt en banque (N°: {depot.num}). Nouveau montant: {depot.montant} DA.",
            ip_address=request.META.get('REMOTE_ADDR')
        )

        return JsonResponse({"status": "success", "message": "Dépôt mis à jour avec succès"})
    except DepotBanque.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Dépôt non trouvé"}, status=404)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)

@login_required(login_url="institut_app:login")
@require_POST
def api_delete_depot_banque(request, pk):
    try:
        depot = DepotBanque.objects.get(pk=pk)
        depot_num = depot.num
        depot_montant = depot.montant
        depot.delete()

        UserActionLog.objects.create(
            user=request.user,
            action_type='DELETE',
            target_model='DepotBanque',
            target_id=str(pk),
            details=f"Suppression du dépôt en banque (N°: {depot_num}) d'un montant de {depot_montant} DA.",
            ip_address=request.META.get('REMOTE_ADDR')
        )

        return JsonResponse({"status": "success", "message": "Dépôt supprimé avec succès"})
    except DepotBanque.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Dépôt non trouvé"}, status=404)
