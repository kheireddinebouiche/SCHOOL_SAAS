from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from django.db.models import Q
from datetime import datetime
from ..models import Derogations


# Modèles (à adapter selon votre structure de données)
# from .models import Derogation

@login_required(login_url='institut_app:login')
def liste_derogations(request):
   
    context = {
        'page_title': 'Liste des dérogations',

    }
    return render(request, 'tenant_folder/crm/liste_derogations.html', context)

@login_required(login_url='institut_app:login')
def ApiLoadDerogation(request):
    liste = Derogations.objects.all()

    data = []
    for i in liste:
        data.append({
            "demandeur" : i.demandeur,
            "type" : i.type,
            "motif" : i.motif,
            "date_de_demande" : i.date_de_demande,
            "statut" : i.statut,
        })

    return JsonResponse(data, safe=False)
