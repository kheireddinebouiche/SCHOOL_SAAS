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
from django.views.decorators.clickjacking import xframe_options_exempt



@login_required(login_url="institut_app:login")
def PageConfPenalite(request):
    entreprises = Entreprise.objects.all()
    return render(request,'tenant_folder/comptabilite/conf/liste_promo.html', locals())


@login_required(login_url="institut_app:login")
def ApiLoadPromo(request):
    if request.method == "GET":
        promo = Promos.objects.all()
        data = []
        for i in promo:
            data.append({
                'id': i.id,
                'begin_year' : i.begin_year,
                'end_year' : i.end_year,
                'session' : i.get_session_display(),
                'prix_rachat_credit' : i.prix_rachat_credit,
                'penalite_retard' : i.penalite_retard,
                'entite_id': i.entite.id if i.entite else None,
                'entite_label': i.entite.designation if i.entite else None,
            })
        return JsonResponse(data, safe=False)

    else:
        return JsonResponse({"status":"error"})

@login_required(login_url="institut_app:login")
def ApiUpdatePromoConfig(request):
    if request.method == 'POST':
        try:
            promo_id = request.POST.get('promo_id')
            prix_rachat_credit = request.POST.get('prix_rachat_credit')
            penalite_retard = request.POST.get('penalite_retard')
            entite_id = request.POST.get('entite_id')

            promo = Promos.objects.get(id=promo_id)
            promo.prix_rachat_credit = Decimal(prix_rachat_credit)
            promo.penalite_retard = Decimal(penalite_retard)
            
            if entite_id:
                promo.entite = Entreprise.objects.get(id=entite_id)
            else:
                promo.entite = None
                
            promo.save()

            return JsonResponse({'status': 'success', 'message': 'Promotion mise à jour avec succès.'})
        except Promos.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Promotion non trouvée.'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée.'}, status=405)


@login_required(login_url="institut_app:login")
def ListePenalite(request):
    return render(request,'tenant_folder/comptabilite/penalite_rachat/demande_paiements.html')


@login_required(login_url="institut_app:login")
def ApiListeDuePenalite(request):
    if request.method == 'GET':
        due_paiements = DuePaiements.objects.filter(type__in=['rach', 'dette', 'autre']).select_related('client')
        data = []
        for due in due_paiements:
            # Check if a payment exists for this due
            paiement = Paiements.objects.filter(due_paiements=due).first()
            data.append({
                'id': due.id,
                'client': f"{due.client.nom} {due.client.prenom}" if due.client else "Client Inconnu",
                'label': due.label,
                'montant_due': due.montant_due,
                'is_done': due.is_done,
                'type': due.get_type_display(),
                'paiement_id': paiement.id if paiement else None,
                'date_echeance': due.date_echeance,
                'date_paiement': paiement.date_paiement if paiement else None,
            })
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée.'}, status=405)


@login_required(login_url="institut_app:login")
def ApiDeleteDuePenalite(request):
    if request.method == 'POST':
        try:
            id_paiement = request.POST.get('id')
            if not id_paiement:
                return JsonResponse({'status': 'error', 'message': 'ID manquant.'}, status=400)

            due_paiement = DuePaiements.objects.get(id=id_paiement)
            due_paiement.delete()

            return JsonResponse({'status': 'success', 'message': 'Paiement dû supprimé avec succès.'})
        except DuePaiements.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Paiement dû introuvable.'}, status=404)


            
@login_required(login_url="institut_app:login")
def ApiPayDuePenalite(request):
    if request.method == 'POST':
        try:
            id_paiement = request.POST.get('id')
            if not id_paiement:
                return JsonResponse({'status': 'error', 'message': 'ID manquant.'}, status=400)

            due_paiement = DuePaiements.objects.get(id=id_paiement)
            if due_paiement.is_done:
                 return JsonResponse({'status': 'info', 'message': 'Ce paiement a déjà été effectué.'})
            
            # Create the actual Payment record
            paiement = Paiements.objects.create(
                due_paiements=due_paiement,
                prospect=due_paiement.client,
                montant_paye=due_paiement.montant_due,
                date_paiement=datetime.now().date(),
                mode_paiement='esp', # Defaulting to Cash as requested
                paiement_label=f"Paiement: {due_paiement.label}",
                context='rach' if due_paiement.type == 'rach' else 'autre', # Mapping logic
                is_done=True,
                # created_by removed as it doesn't exist in model
            )
            
            due_paiement.is_done = True
            due_paiement.save()

            return JsonResponse({
                'status': 'success', 
                'message': 'Paiement effectué avec succès.',
                'paiement_id': paiement.id
            })
        except DuePaiements.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Paiement dû introuvable.'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée.'}, status=405)


@xframe_options_exempt
@login_required(login_url="institut_app:login")
def PrintReceipt(request, paiement_id):
    try:
        paiement = Paiements.objects.get(id=paiement_id)
        return render(request, 'tenant_folder/comptabilite/penalite_rachat/print_receipt.html', {'paiement': paiement})
    except Paiements.DoesNotExist:
        messages.error(request, "Paiement introuvable.")
        return render(request, 'tenant_folder/404.html') # Or redirect back
