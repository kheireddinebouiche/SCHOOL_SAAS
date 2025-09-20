from django.shortcuts import render
from django.http import JsonResponse
from ..models import *
from django.db import transaction
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
import json
from t_crm.models import RemiseAppliquer



@login_required(login_url="institut_app:login")
def ApiGetPaiementRequestDetails(request):
    id_client = request.GET.get('id_client')
    
    obj_client = Prospets.objects.get(id= id_client)
    
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
            ApiStorePaiements(obj_client,i['libelle'],i['date_echeance'],i['montant'])  
            print(i['libelle'], i['montant'])   
             
        return JsonResponse({"status":"success"})
    
    else:
        
        return JsonResponse({'error': 'Aucune donnée d\'échéancier fournie'}, status=400)

### Fonction qui stock les echeanciers de paiements
def ApiStorePaiements(client,label,date_echeance,montant):
    try:
        DuePaiements.objects.create(
            client = client,
            label = label,
            montant_due = montant,
            date_echeance = date_echeance
        )
    except:
        return JsonResponse({"status" : "error"})
    
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
