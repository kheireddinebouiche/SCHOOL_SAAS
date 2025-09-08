from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from ..models import *
from django.contrib.auth.decorators import login_required

@login_required(login_url='institut_app:login')
def detailsEntreprise(request, pk):
    context = {
        'tenant' : request.tenant,
        'pk' : pk
    }
    return render(request, 'tenant_folder/entreprise/details_entreprise.html', context)

@login_required(login_url="institut_app:login")
def ApiLoadEntrepriseData(request):
    id_entreprise = request.GET.get('id_entreprise')
    
       
    entreprise = Entreprise.objects.get(id=id_entreprise)

    data = {
        'id' : entreprise.id,
        'designation' : entreprise.designation,
        'rc' : entreprise.rc,
        'nif' : entreprise.nif,
        'art' : entreprise.art,
        'nis' : entreprise.nis,
        'adresse' : entreprise.adresse,
        'telephone' : entreprise.telephone,
        'wilaya' : entreprise.wilaya,
        'pays' : entreprise.pays.name,
        'email' : entreprise.email,
        'site_web' : entreprise.site_web,
    }

    return JsonResponse(data, safe=False)

@login_required(login_url="institut_app:login")
def ApiUpdateEntrepriseData(request):
    pass


@login_required(login_url="institut_app")
def ApiListeBanckAccountEntreprise(request):
    pass

@login_required(login_url="institut_app")
def ApiSaveBankAccount(request):
    pass




