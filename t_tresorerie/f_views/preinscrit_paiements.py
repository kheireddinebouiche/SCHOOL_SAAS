from django.shortcuts import render
from django.http import JsonResponse
from ..models import *
from django.db import transaction
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
import json
from t_crm.models import RemiseAppliquer,FicheDeVoeux
from django.db.models import Q
from institut_app.decorators import *


@login_required(login_url="institut_app:login")
@ajax_required
def ApiGetPaiementRequestDetails(request):
    id_client = request.GET.get('id_client')
    
    obj_client = Prospets.objects.get(id= id_client)

    # Récuperer la promo de l etudiant
    obj_promo  = FicheDeVoeux.objects.get(prospect = obj_client, is_confirmer=True)
    
    # Récupérer les données de l'échéancier depuis la requête
    echeancier_data = request.GET.get('echeancier_data')
    
    if echeancier_data:
        # Parser les données de l'échéancier
        echeancier_list = json.loads(echeancier_data)
        
        # Calculer les totaux
        total_initial = sum(Decimal(e['montant']) for e in echeancier_list)
        total_final = sum(Decimal(e['montant_final']) for e in echeancier_list)
        
        # Préparer les données de réponse
        data = {
            'client': {
                'id': id_client,
            },
            'echeancier': echeancier_list,
            'total_initial': str(total_initial),
            'total_final': str(total_final),
            'reduction': request.GET.get('reduction', '0') + '%' if request.GET.get('has_reduction') else '0%'
        }
        ### Boucle pour enregistrer les paiements
        for i in echeancier_list:
            ApiStorePaiements(obj_client,i['libelle'],i['date_echeance'],i['montant_final'],obj_promo)  
               
             
        return JsonResponse({"status":"success"})
    
    else:
        
        return JsonResponse({'error': 'Aucune donnée d\'échéancier fournie'}, status=400)

### Fonction qui stock les echeanciers de paiements
def ApiStorePaiements(client,label,date_echeance,montant,promo):
    try:
        last = DuePaiements.objects.filter(client=client).order_by('-ordre').first()
        ordre = (last.ordre + 1) if last else 1

        DuePaiements.objects.create(
            client=client,
            label=label,
            ordre=ordre,
            montant_due=montant,
            montant_restant=montant,
            date_echeance=date_echeance,
            promo = promo,
        )
        return JsonResponse({"status": "success"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})
    
@login_required(login_url="institut_app:login")
def ApiApplyRemiseToPaiement(request):
    if request.method == "POST":
        remiseId = request.POST.get('remiseId')

        remise_obj = RemiseAppliquer.objects.get(id = remiseId)
        remise_obj.is_approuved = True
        remise_obj.save()

        return JsonResponse({"status" : "success"})
    else:
        return JsonResponse({"status" : "error"})

@login_required(login_url="institut_app:login")
@transaction.atomic
def ApiStoreClientPaiement(request):
    echeance = request.POST.get('echeance')
    datePaiement = request.POST.get('datePaiement')
    montant = request.POST.get('montant')
    modePaiement = request.POST.get('modePaiement')
    reference = request.POST.get('reference')
    observation = request.POST.get('observation')
    clientId = request.POST.get('clientId')
    id_due_paiement = request.POST.get('id_due_paiement')
    promo = request.POST.get('promo')

    try:
        due_paiement = DuePaiements.objects.get(id=id_due_paiement)

        if due_paiement.ordre and due_paiement.ordre > 1:
            previous_due = DuePaiements.objects.filter(client_id=clientId,ordre=due_paiement.ordre - 1).first()
            if previous_due and not previous_due.is_done:
                return JsonResponse({"status": "error","message": "Le paiement précédent n'est pas encore effectué."})
    
        Paiements.objects.create(
            due_paiements = DuePaiements.objects.get(id = id_due_paiement),
            prospect = Prospets.objects.get(id = clientId),
            montant_paye = montant,
            date_paiement = datePaiement,
            observation = observation,
            mode_paiement = modePaiement,
            reference_paiement = reference,
            context = "frais_f",
            promo = Promos.objects.get(code = promo) if promo else None,
        )

        if(montant == DuePaiements.objects.get(id = id_due_paiement).montant_restant):
            montant_restant = 0
        else:
            montant_restant = Decimal(DuePaiements.objects.get(id = id_due_paiement).montant_restant) - Decimal(montant)

        update_due_paiement= DuePaiements.objects.get(id = id_due_paiement)
        update_due_paiement.is_done = True
        update_due_paiement.montant_restant = montant_restant
        update_due_paiement.save()

        return JsonResponse({"status" : "success"})
    

    except DuePaiements.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Échéance introuvable."})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})
 
@login_required(login_url="institut_app:login")
@transaction.atomic
def ApiDeletePaiement(request):
    if request.method == "POST":
        num_bon = request.POST.get('num_bon')   
        paiement_obj = Paiements.objects.get(num = num_bon) 
        
        montant_paye = paiement_obj.montant_paye

        paiement_obj.due_paiements.montant_restant = Decimal(paiement_obj.due_paiements.montant_restant) + Decimal(montant_paye)
        paiement_obj.due_paiements.is_done = False
        paiement_obj.due_paiements.save()

        paiement_obj.delete()

        return JsonResponse({"status" : "success"})
    else:
        return JsonResponse({"status" : "error"})
    
@login_required(login_url="institut_app:login")
@transaction.atomic
def ApiApplyEcheancierSpecial(request):
    if request.method == "POST":
        id_echeancier_special = request.POST.get('id_echeancier_special')
        obj_echeancier_special = EcheancierSpecial.objects.get(id = id_echeancier_special)
        obj_echeancier_special.is_validate = True
        obj_echeancier_special.save()
        return JsonResponse({"status" : "success"})
    else:
        return JsonResponse({"status" : "error"})

@login_required(login_url="institut_app:login")
@transaction.atomic
def ApiConfirmInscription(request):
    if request.method == "POST":
        id_client = request.POST.get('id_preinscrit')
        client = Prospets.objects.get(id = id_client)
        client.statut = 'convertit'
        client.save()

        return JsonResponse({"status" : "success"})
    else:   
        return JsonResponse({"status" : "error"})
    
@login_required(login_url="institut_app:login")
@transaction.atomic
def ApiRequestRefundPaiement(request):
    if request.method == "POST":
        id_client = request.POST.get('client_id')
        reason = request.POST.get('reason')
        Rembourssements.objects.create(
            client = Prospets.objects.get(id = id_client),
            motif_rembourssement = reason,
            etat = 'enc',
            is_done = False
        )
       
        return JsonResponse({"status" : "success"})
    else:
        return JsonResponse({"status" : "error"})
    
@login_required(login_url="institut_app:login")
def SuivieEcheancier(request):
    return render(request, 'tenant_folder/comptabilite/echeancier/suivie_echeancier.html')