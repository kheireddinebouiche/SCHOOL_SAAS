from django.shortcuts import render
from django.http import JsonResponse
from ..models import *
from django.contrib.auth.decorators import login_required
from ..forms import *
from t_crm.models import NotesProcpects, RendezVous
from django.db import transaction



@login_required(login_url="institut_app:login")
def RegistrePage(request):

    groupes = Groupe.objects.all()
    registres = RegistrePresence.objects.all()

    context = {
        'groupes' : groupes,
        'registres' : registres,
    }
    return render(request, 'tenant_folder/presences/registres.html', context)


@login_required(login_url="institut_app:login")
@transaction.atomic
def ApiSaveRegistreGroupe(request):
    registerName = request.POST.get('registerName')
    semester = request.POST.get('semester')
    group = request.POST.get('group')


    try:
        RegistrePresence.objects.create(
            label = registerName,
            semestre = semester,
            groupe_id = group,
        )

        return JsonResponse({"status" : "success"})
    except:
        return JsonResponse({"status" : "error"})
    

@login_required(login_url="institut_app:login")
def DetailsRegistrePresence(request, pk):
    registre = RegistrePresence.objects.get(id= pk)

    context = {
        'registre' : registre
    }

    return render(request, 'tenant_folder/presences/details_registre.html', context)

@login_required(login_url="institut_app:login")
def liste_registres(request):
    pass