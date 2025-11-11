from django.shortcuts import render
from django.http import JsonResponse
from ..models import *
from django.db import transaction
from decimal import Decimal
from django.contrib.auth.decorators import login_required


@login_required(login_url="institut_app:login")
def PageDepenses(request):
    return render(request,'tenant_folder/comptabilite/depenses/liste_des_depenses.html')

@login_required(login_url="institut_app:ApiListeDepenses")
def ApiListeDepenses(request):
    liste = Depenses.objects.all().values('id')
    return JsonResponse(list(liste), safe=False)


@login_required(login_url="institut_app:login")
def PageNouvelleDepense(request):
    return render(request, "tenant_folder/comptabilite/depenses/nouvelle_depense.html")

@login_required(login_url="institut_app:login")
def ApiLoadTypeDepense(request):
    if request.method == 'GET':
        liste = TypeDepense.objects.all().values('id','label')
        return JsonResponse(list(liste), safe=False)
    else:
        return JsonResponse({"status":"error",'message':'methode non autoriser'})
    

@login_required(login_url="institut_app:login")
def ApiStoreNewType(request):
    if request.method == "POST":
        typeName = request.POST.get('typeName')
        typeDescription = request.POST.get('typeDescription')
    else:
        return JsonResponse({"status":"error",'message':"methode non autoriser"})


