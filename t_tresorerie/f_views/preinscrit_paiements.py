from django.shortcuts import render
from django.http import JsonResponse
from ..models import *
from django.db import transaction
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
import json



@login_required(login_url="institut_app:login")
def ApiGetPaiementRequestDetails(request):
    id_client = request.GET.get('id_client')
    
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
            ApiStorePaiements(i['montant'])     
             
        return JsonResponse(data)
    else:
        
        return JsonResponse({'error': 'Aucune donnée d\'échéancier fournie'}, status=400)

### Fonction qui stock les echeanciers de paiements
@login_required(login_url="institut_app:login")
def ApiStorePaiements(montant):
    print(montant)
