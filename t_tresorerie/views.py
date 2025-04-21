from django.shortcuts import render
from django.http import JsonResponse
from .models import *




def AttentesPaiements(request):
    
    context = {
       
        'tenant' : request.tenant,
    }

    return render(request, 'tenant_folder/comptabilite/tresorerie/attentes_de_paiement.html', context)

def ApiListeDemandePaiement(request):
    liste = ClientPaiementsRequest.objects.all().values('id', 'specialite__label','specialite__prix', 'formation__nom','formation__frais_assurance','formation__frais_inscription', 'demandes__visiteur__nom', 'demandes__visiteur__prenom','amount','created_at','etat')
    return JsonResponse(list(liste), safe=False)

def PageDetailsDemandePaiement(request, pk):
    context = {
        'tenant' : request.tenant,
        'pk' : pk,
    }
    return render(request, "tenant_folder/comptabilite/tresorerie/details_attente_paiement.html", context)

def ApiGetDetailsDemandePaiement(request):
    id= request.GET.get('id_demande')
    pass

def ApiDeleteDemandePaiement(request):
    id_demande = request.GET.get('id_demande')
    obj = ClientPaiementsRequest(id = id_demande)
    obj.delete()

    return JsonResponse({'status' : 'success', "message" : "La suppréssion a été effectuer avec succès"})
