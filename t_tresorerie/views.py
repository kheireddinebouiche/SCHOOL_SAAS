from django.shortcuts import render
from django.http import JsonResponse
from .models import *




def AttentesPaiements(request):
    
    context = {
       
        'tenant' : request.tenant,
    }

    return render(request, 'tenant_folder/comptabilite/tresorerie/attentes_de_paiement.html', context)

def ApiListeDemandePaiement(request):
    liste = ClientPaiementsRequest.objects.all().values('id', 'specialite__label','specialite__prix', 'formation__nom', 'client__nom', 'client__prenom','amount','created_at')
    return JsonResponse(list(liste), safe=False)


def ApiDeleteDemandePaiement(request):
    id_demande = request.GET.get('id_demande')
    obj = ClientPaiementsRequest(id = id_demande)
    obj.delete()

    return JsonResponse({'status' : 'success', "message" : "La suppréssion a été effectuer avec succès"})
