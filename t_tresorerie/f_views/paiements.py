from django.shortcuts import render
from django.http import JsonResponse
from ..models import *
from django.db import transaction
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
import json
from t_crm.models import RemiseAppliquer, Prospets,FicheDeVoeux, FicheVoeuxDouble
from django.db.models import Q, Sum, F, Case, When, Value, CharField, Count


@login_required(login_url="institut_app:login")
def ListeDesPaiements(request):
    return render(request, 'tenant_folder/comptabilite/paiements/liste_des_paiements.html')

@login_required(login_url="institut_app:login")
def ApiListePaiements(request):
    liste = Paiements.objects.filter(is_refund=False)

    data = []
    for i in liste:
        # Récupération de la spécialité associée au prospect
        try:
            fiche = FicheDeVoeux.objects.get(prospect_id=i.prospect_id)
            specialite = fiche.specialite.label if fiche.specialite else None
        except FicheDeVoeux.DoesNotExist:
            
            fiche = FicheVoeuxDouble.objects.get(prospect_id=i.prospect_id)
            specialite = fiche.specialite.label

        data.append({
            'id': i.id,
            'num': i.num,
            'prospect_nom': i.prospect.nom,
            'prospect_prenom': i.prospect.prenom,
            'specialite': specialite,
            'montant_paye': i.montant_paye,
            'date_paiement': i.date_paiement,
            'mode_paiement': i.get_mode_paiement_display(),
            'context': i.get_context_display(),
            'context_key': i.context,
            'facture_num' : i.facture.num_facture if i.facture else None,
            'facture_id' : i.facture.id if i.facture else None,
            'payment_type_id': i.payment_type.id if i.payment_type else None,
            'payment_type_name': i.payment_type.name if i.payment_type else "Non défini",
        })

    return JsonResponse(data, safe=False)

@login_required(login_url="institut_app:login")
def PageCategoriesProduits(request):
    """Page to manage payment categories"""
    return render(request, 'tenant_folder/comptabilite/produits/liste_categories_produits.html')

@login_required(login_url="institut_app:login")
@require_http_methods(["POST"])
def ApiUpdatePaymentType(request):
    try:
        data = json.loads(request.body)
        paiement_id = data.get('paiement_id')
        payment_type_id = data.get('payment_type_id')
        
        if not paiement_id or not payment_type_id:
            return JsonResponse({'status': 'error', 'message': 'Données manquantes'}, status=400)
            
        paiement = Paiements.objects.get(id=paiement_id)
        payment_type = PaymentType.objects.get(id=payment_type_id)
        
        paiement.payment_type = payment_type
        paiement.save()
        
        return JsonResponse({'status': 'success', 'message': 'Type de paiement mis à jour avec succès'})
    except Paiements.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Paiement introuvable'}, status=404)
    except PaymentType.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Type de paiement introuvable'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


    
