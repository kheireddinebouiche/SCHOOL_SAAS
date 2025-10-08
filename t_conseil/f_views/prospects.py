from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from t_crm.models import Prospets


@login_required(login_url="institut_app:login")
def ApiListeProspect(request):
    liste = Prospets.objects.filter(type_prospect = "entreprise").values('id','nom','prenom','etat','entreprise','poste_dans_entreprise','observation','context','created_at','telephone','email')
    return JsonResponse(list(liste), safe=False)


    
    
    
    
    
    