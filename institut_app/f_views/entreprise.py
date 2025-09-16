from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from ..models import *
from django.contrib.auth.decorators import login_required
from django.db import transaction

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
    id_entreprise = request.GET.get('id_entreprise')

    bankAccounts = BankAccount.objects.filter(entreprise = Entreprise.objects.get(id = id_entreprise), is_archived=False).values('id','bank_name','bank_iban','bank_currency')
   

    return JsonResponse(list(bankAccounts), safe=False)

@login_required(login_url="institut_app")
@transaction.atomic
def ApiSaveBankAccount(request):
    id_entreprise = request.POST.get('id_entreprise')
    bank_name = request.POST.get('bank_name')
    bank_iban = request.POST.get('bank_iban')
    bank_currency = request.POST.get('bank_currency')
    bank_observations = request.POST.get('bank_observations')

    entreprise = Entreprise.objects.get(id = id_entreprise)
    try:
        BankAccount.objects.create(
            entreprise = entreprise,
            bank_name = bank_name,
            bank_iban = bank_iban,
            bank_currency = bank_currency,
            bank_observations = bank_observations
        )
        return JsonResponse({"status" : "success"})

    except:
        return JsonResponse({"status" : "error"})

@login_required(login_url="institut_app:login")
def ApiLoadBankAccountDetails(request):
    account_id = request.GET.get('account_id') 
    bankaccountdetail = BankAccount.objects.get(id = account_id)

    data = {
        'bank_name' : bankaccountdetail.bank_name,
        'bank_iban' : bankaccountdetail.bank_iban,
        'bank_currency' : bankaccountdetail.bank_currency,
        'bank_observations' : bankaccountdetail.bank_observations,
    }

    return JsonResponse({'data' : data})

@login_required(login_url="institut_app:login")
def ApiArchiveBankAccount(request):
    account_id = request.POST.get('account_id')
    account = BankAccount.objects.get(id = account_id)

    account.is_archived = True
    account.save()

    return JsonResponse({"status" : "success"})



