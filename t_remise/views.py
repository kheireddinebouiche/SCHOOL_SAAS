from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from django.db import transaction
from decimal import Decimal
from django.contrib.auth.decorators import login_required


@login_required(login_url="institut_app:login")
def ListeRemise(request):
    context = {
        'tenant' : request.tenant
    }
    return render(request,'tenant_folder/remises/liste_des_remises.html', context)


@login_required(login_url="institut_app:login")
def ApiListeRemise(request):
    liste = Remises.objects.all().values('id','label','taux','is_enabled','created_at','has_to_justify','description', 'is_value', 'montant').order_by('-created_at')
    return JsonResponse(list(liste), safe=False)


@login_required(login_url="institut_app:login")
def ApiDetailsRemise(request):
    id_remise = request.GET.get('id_remise')
    obj = Remises.objects.get(id = id_remise)

    data = {
        'id' : obj.id,
        "label" : obj.label,
        "taux" : obj.taux,
        "is_enabled" : obj.is_enabled,
        "is_value" : obj.is_value,
        "montant" : obj.montant,
        "description" : obj.description,
        "has_to_justify" : obj.has_to_justify
    }

    return JsonResponse(data, safe=False)


@login_required(login_url="institut_app:login")
@transaction.atomic
def ApiActivateRemise(request):
    id_remise = request.POST.get('id_remise')
    obj = Remises.objects.get(id = id_remise)

    obj.is_enabled = True
    obj.save()

    return JsonResponse({"status" : "success"})

@login_required(login_url="institut_app:login")
@transaction.atomic
def ApiDeactivateRemise(request):
    id_remise = request.POST.get('id_remise')
    obj = Remises.objects.get(id = id_remise)

    obj.is_enabled = False
    obj.save()

    return JsonResponse({"status" : "success"})


@login_required(login_url="institut_app:login")
@transaction.atomic
def ApiUpdateRemise(request):
    id_remise = request.POST.get('id_remise')
    label = request.POST.get('label')
    taux = request.POST.get('taux')
    is_value = request.POST.get('is_value') == 'True'
    montant = request.POST.get('montant')
    description = request.POST.get('description')
    justificatif = request.POST.get('justificatif_requis')
    
    obj = Remises.objects.get(id = id_remise)
    obj.label = label
    obj.taux = taux if not is_value else None
    obj.is_value = is_value
    obj.montant = montant if is_value else None
    obj.description = description
    obj.has_to_justify = justificatif
    obj.save()

    return JsonResponse({'status': "success"})

@login_required(login_url="institut_app:login")
@transaction.atomic
def ApiDeleteRemise(request):
    id_remise = request.POST.get('id_remise')
    obj = Remises.objects.get(id = id_remise)
    obj.delete()
    return JsonResponse({'status': "success"})

@login_required(login_url="institut_app:login")
@transaction.atomic
def ApiCreateRemise(request):
    label = request.POST.get('label')
    taux = request.POST.get('taux')
    is_value = request.POST.get('is_value') == 'True'
    montant = request.POST.get('montant')
    description = request.POST.get('description')
    justificatif = request.POST.get('justificatif_requis')
    
    Remises.objects.create(
        label = label,
        taux = taux if not is_value else None,
        is_value = is_value,
        montant = montant if is_value else None,
        is_enabled = False, 
        description = description,
        has_to_justify = justificatif,
    )

    return JsonResponse({'status': "success"})