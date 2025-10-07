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
    liste = Remises.objects.all().values('id','label','taux','is_enabled','created_at','has_to_justify','description').order_by('-created_at')
    return JsonResponse(list(liste), safe=False)


@login_required(login_url="institut_app:login")
def ApiDetailsRemise(request):
    id_remise = request.GET.get('id_remise')
    obj = Remises.objects.get(id = id_remise)

    data = {
        'id' : obj.id,
        "label" : obj.label,
        "taux" : obj.taux,
        "is_enabled" : obj.is_enabled
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
def ApiArchiveRemise(request):
    pass

@login_required(login_url="institut_app:login")
def ApiUpdateRemise(request):
    pass

@login_required(login_url="institut_app:login")
@transaction.atomic
def ApiCreateRemise(request):
    label = request.POST.get('label')
    taux = request.POST.get('taux')
    description = request.POST.get('description')
    justificatif = request.POST.get('justificatif_requis')
    print(justificatif)
    
    # if justificatif == "on":
    #     justificatif = True
    # else:
    #     justificatif = False
    
    # Remises.objects.create(
    #     label = label,
    #     taux = taux,
    #     is_enabled = False, 
    #     description = description,
    #     #has_to_justify = justificatif
    # )

    return JsonResponse({'status': "success"})