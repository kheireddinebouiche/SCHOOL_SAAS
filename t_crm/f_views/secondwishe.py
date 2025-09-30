from django.shortcuts import render,redirect
from django.http import JsonResponse
from ..models import *
from ..forms import *
from django.contrib import messages
from t_formations.models import *
from django.db import transaction
from django.db.models import Count, Q
from django.core.exceptions import PermissionDenied
from functools import wraps
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.utils.dateformat import format



@login_required(login_url='institut_app:login')
def ApiListeSecondWishes(request):
    id_prospect = request.GET.get('id_prospect')

    liste =  FicheDeVoeuxAddiotionnel.objects.filter(prospect__id = id_prospect).values('id','promo__session','promo__begin_year','promo__end_year','specialite','specialite__label')
    
    return JsonResponse(list(liste), safe=False)

@login_required(login_url="institut_app:login")
@transaction.atomic
def ApiStoreSecondWish(request):
    promo = request.POST.get('promo')
    specialite = request.POST.get('specialite')
    commentaires = request.POST.get('commentaires')
    id_prospect = request.POST.get('id_prospect')

    obj_spec = Specialites.objects.get(id = specialite)
    print(Specialites.objects.get(id = specialite))

    FicheDeVoeuxAddiotionnel.objects.create(
        promo = Promos.objects.get(code = promo),
        specialite =obj_spec,
        prospect = Prospets.objects.get(id = id_prospect),
        commentaire = commentaires,
    )

    return JsonResponse({"status" : "success"})

@login_required(login_url="institut_app:login")
def ApiDeleteSecondWish(request):
    id_second_voeux = request.POST.get('id_voeux_supp')
    obj = FicheDeVoeuxAddiotionnel.objects.get(id = id_second_voeux)
    obj.delete()

    return JsonResponse({'status' : 'success'})

@login_required(login_url="institut_app:login")
@transaction.atomic
def ApiConfirmeSecondWish(request):
    id_prospect = request.POST.get('id_prospect')
    id_voeux_sup = request.POST.get('id_voeux_sup')

    print(id_prospect, id_voeux_sup)

    prospect = Prospets.objects.get(id = id_prospect)
    voeux_principal = FicheDeVoeux.objects.filter(prospect = prospect, is_confirmed=False).last()

    voeux_supplementaire = FicheDeVoeuxAddiotionnel.objects.get(id = id_voeux_sup)
    specialite_remplacement = voeux_supplementaire.specialite

    voeux_principal.specialite = specialite_remplacement
    voeux_principal.save()

    return JsonResponse({'status' : 'success'})

@login_required(login_url="institut_app:login")
def ApiCountFormationSupplementaire(request):
    id_prospect = request.GET.get('id_prospect')
    count = FicheDeVoeuxAddiotionnel.objects.filter(prospect__id=id_prospect).count()
    return JsonResponse({"count" : count})
