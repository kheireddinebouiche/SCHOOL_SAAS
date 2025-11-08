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
        'pays' : entreprise.pays,
        'email' : entreprise.email,
        'site_web' : entreprise.site_web,
        'code_postal' : entreprise.code_postal,
        'ville' : entreprise.ville,
        'numero' : entreprise.numero,
        'code_wilaya' : entreprise.code_wilaya,
        'representant' : entreprise.representant,
    }

    return JsonResponse(data, safe=False)

@login_required(login_url="institut_app:login")
@transaction.atomic
def ApiUpdateEntrepriseData(request):
    if request.method =="POST":
        id_entreprise = request.POST.get('id_entreprise')
        designation = request.POST.get('designation')
        adresse = request.POST.get('adresse')
        wilaya = request.POST.get('wilaya')
        pays = request.POST.get('pays')
        code_postal = request.POST.get('code_postal')
        email = request.POST.get('email')
        telephone = request.POST.get('telephone')
        site_web = request.POST.get('site_web')
        rc = request.POST.get('rc')
        art = request.POST.get('art')
        nif = request.POST.get('nif')
        nis = request.POST.get('nis')
        observations = request.POST.get('observations')
        ville = request.POST.get('ville')
        numero = request.POST.get('numero')
        code_wilaya = request.POST.get('code_wilaya')
        representant = request.POST.get('representant')

        entreprise = Entreprise.objects.get(id = id_entreprise)
        
        entreprise.designation = designation
        entreprise.adresse = adresse
        entreprise.wilaya = wilaya
        entreprise.pays = pays
        entreprise.code_postal = code_postal
        entreprise.email = email
        entreprise.rc = rc
        entreprise.nif = nif
        entreprise.art = art
        entreprise.nis = nis
        entreprise.site_web = site_web
        entreprise.telephone = telephone
        entreprise.observations = observations
        entreprise.ville = ville
        entreprise.numero = numero
        entreprise.code_wilaya = code_wilaya
        entreprise.representant = representant
        entreprise.save()

        return JsonResponse({'status':"success",'message':'Les informations ont été mis a jour avec succès'})
    else:
        return JsonResponse({'status':"error",'message':'Methode non autoriser'})

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


@login_required(login_url="institut_app:login")
def ApiUpdateEntrepriseLogos(request):
    if request.method == "POST":
        id_entreprise = request.POST.get('id_entreprise')
        
        entreprise = Entreprise.objects.get(id=id_entreprise)
        
        # Handle logo updates
        if 'logo' in request.FILES:
            entreprise.logo = request.FILES['logo']
        
        if 'entete_logo' in request.FILES:
            entreprise.entete_logo = request.FILES['entete_logo']
        
        if 'pied_page_logo' in request.FILES:
            entreprise.pied_page_logo = request.FILES['pied_page_logo']
        
        entreprise.save()
        
        return JsonResponse({
            'status': 'success', 
            'message': 'Logos mis à jour avec succès',
            'logo_url': entreprise.logo.url if entreprise.logo else None,
            'entete_logo_url': entreprise.entete_logo.url if entreprise.entete_logo else None,
            'pied_page_logo_url': entreprise.pied_page_logo.url if entreprise.pied_page_logo else None
        })
    else:
        return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'})


@login_required(login_url="institut_app:login")
def ApiLoadEntrepriseLogos(request):
    id_entreprise = request.GET.get('id_entreprise')
    
    entreprise = Entreprise.objects.get(id=id_entreprise)

    data = {
        'id': entreprise.id,
        'logo_url': entreprise.logo.url if entreprise.logo else None,
        'entete_logo_url': entreprise.entete_logo.url if entreprise.entete_logo else None,
        'pied_page_logo_url': entreprise.pied_page_logo.url if entreprise.pied_page_logo else None,
    }

    return JsonResponse(data, safe=False)



