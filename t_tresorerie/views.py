from django.shortcuts import render
from .models import *




def AttentesPaiements(request):
    liste = ClientPaiementsRequest.objects.filter(paid=False)
    context = {
        'liste' : liste,
        'tenant' : request.tenant,
    }

    return render(request, 'tenant_folder/comptabilite/tresorerie/attentes_de_paiement.html', context)