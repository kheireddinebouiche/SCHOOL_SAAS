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
from django.db.models import F, Value, CharField, Q, Case, When
from django.db.models.functions import Coalesce
from itertools import chain
from django.db.models.functions import Concat
from django.contrib.humanize.templatetags.humanize import intcomma


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
    autres_produits = AutreProduit.objects.filter(mode_paiement='esp', date_paiement__gte=start_date, date_paiement__lte=end_date).exclude(date_paiement__isnull=True).values(
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
        consulting_paiements = ConseilPaiement.objects.filter(mode_paiement='espece', date_paiement__gte=start_date, date_paiement__lte=end_date).exclude(date_paiement__isnull=True).values(
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
    depenses = Depenses.objects.filter(mode_paiement='esp', date_paiement__gte=start_date, date_paiement__lte=end_date).exclude(date_paiement__isnull=True).values(
        nom=F('label'),
        date=F('date_paiement'),
        mouvement_montant=F('montant_ttc'),
        type=Value('sortie', output_field=CharField()),
        descr=F('description'),
        ref=Coalesce('reference', Value('')),
        order_to=Case(
            When(fournisseur__isnull=False, then=F('fournisseur__designation')),
            When(client__isnull=False, then=Concat(F('client__nom'), Value(' '), F('client__prenom'))),
            default=Value('Inconnu'),
            output_field=CharField()
        ),
        entite_name=F('entite__designation')
    )

    # ---- 3. Fusion et tri chronologique ----
    mouvements = sorted(
        chain(paiements, autres_produits, consulting_paiements, depenses),
        key=lambda x: (
            x['date'] if isinstance(x['date'], datetime) 
            else datetime.combine(x['date'], datetime.min.time())
        ) if x['date'] else datetime.min
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

    # Fiscal Year Filtering
    today = datetime.now().date()
    default_year = today.year if today.month >= 8 else today.year - 1
    try:
        year = int(request.GET.get('year', default_year))
    except ValueError:
        year = default_year
        
    start_date = datetime(year, 8, 1).date()
    end_date = datetime(year + 1, 7, 31).date()

    # ---- 1. Paiements (Entrées en banque) ----
    paiements = Paiements.objects.filter(mode_paiement__in=['vir', 'che'], date_paiement__gte=start_date, date_paiement__lte=end_date).exclude(date_paiement__isnull=True).values(
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
    autres_produits = AutreProduit.objects.filter(mode_paiement__in=['che', 'vir'], date_paiement__gte=start_date, date_paiement__lte=end_date).exclude(date_paiement__isnull=True).values(
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
        consulting_paiements = ConseilPaiement.objects.filter(mode_paiement__in=['virement', 'cheque'], date_paiement__gte=start_date, date_paiement__lte=end_date).exclude(date_paiement__isnull=True).values(
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
    depenses = Depenses.objects.filter(mode_paiement__in=['vir', 'che'], date_paiement__gte=start_date, date_paiement__lte=end_date).exclude(date_paiement__isnull=True).values(
        nom=F('label'),
        date=F('date_paiement'),
        mouvement_montant=F('montant_ttc'),
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
                        'fournisseur' : i.depense.fournisseur.designation if i.depense.fournisseur else "Divers",
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
            if p_type == 'standard':
                paiement = Paiements.objects.get(id=paiement_id)
            elif p_type == 'autre':
                paiement = AutreProduit.objects.get(id=paiement_id)
            elif p_type == 'conseil':
                from t_conseil.models import Paiement as ConseilPaiement
                paiement = ConseilPaiement.objects.get(id=paiement_id)
            else:
                return JsonResponse({"status": "error", "message": "Type de paiement invalide"})

            paiement.date_paiement = effective_date
            paiement.is_done = True
            paiement.save()
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
